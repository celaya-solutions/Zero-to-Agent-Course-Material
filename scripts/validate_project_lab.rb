#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

ROOT = File.expand_path("..", __dir__)
COURSE = File.join(ROOT, "courses", "project-lab")
LANDING = File.join(ROOT, "course", "landing.html")
REQUIRED_LEVEL_FILES = %w[level.yml student.md instructor.md worksheet.md slides.html].freeze
REQUIRED_LEVEL_PDFS = %w[student.pdf instructor.pdf worksheet.pdf].freeze
MANIFEST_KEYS = %w[number title objective prerequisites passing_proof required_project_milestone core_route builder_extension].freeze
SHARED_FILES = %w[answer-key.md safety-card.md test-sheet.md case-study.md access-and-outage.md language-plan.md demo-rubric.md].freeze
LINKED_SHARED_PDFS = %w[answer-key.pdf safety-card.pdf test-sheet.pdf access-and-outage.pdf demo-rubric.pdf].freeze
REQUIRED_ASSETS = {
  1 => %w[public-identity-and-work.md public-contact-and-method.md training-record-a.md training-record-b.md rules-card.md fallback-grounded-run.md saved-runs.json],
  2 => %w[practice-page.html fallback-three-runs.md starter/README.md starter/watch.py starter/test_watch.py starter/watch.yml],
  3 => %w[command-card.md Modelfile.template benchmark-card.md fallback-benchmark.md prompts.json],
  4 => %w[callers.json attacks.json csr-public-brief.md training-faq.md desk-instructions.md caller-card.md fallback-caller-run.md mail-desk-vulnerable.md mail-desk-fixed.md attack-card.md fallback-before-after.md],
  5 => %w[outage-presentation-packet.md project-paths.md cost-sheet.md proof-board.md presentation-card.md],
}.freeze

errors = []

def normalized(text)
  text.to_s.gsub(/\s+/, " ").strip
end

def schedule_total(path)
  content = File.read(path)
  section = content[/^## 90-minute schedule\s*$\n(.*?)(?=^## |\z)/m, 1]
  return nil unless section

  section.scan(/^\| (?!\*\*Total)(?:.*?) \| (\d+) \|$/).flatten.map(&:to_i).sum
end

course_manifest_path = File.join(COURSE, "course.yml")
unless File.file?(course_manifest_path)
  errors << "Missing courses/project-lab/course.yml"
else
  course = YAML.safe_load_file(course_manifest_path)
  errors << "Project Lab must contain five levels" unless course["level_count"] == 5
  errors << "Each Project Lab level must be 90 minutes" unless course["duration_minutes_per_level"] == 90
  errors << "English must be the primary language" unless course["primary_language"] == "en"
  errors << "Spanish phase status is missing" unless course["translation_status"].to_s.include?("Spanish")
  errors << "Official case-study source is missing" unless course.dig("case_study", "public_source") == "https://www.celayasolutions.com/"
end

%w[README.md index.html].each do |name|
  path = File.join(COURSE, name)
  errors << "Missing courses/project-lab/#{name}" unless File.file?(path) && !File.zero?(path)
end

errors << "Missing courses/project-lab/README.pdf" unless File.file?(File.join(COURSE, "README.pdf"))

SHARED_FILES.each do |name|
  path = File.join(COURSE, "_shared", name)
  errors << "Missing courses/project-lab/_shared/#{name}" unless File.file?(path) && !File.zero?(path)
end

LINKED_SHARED_PDFS.each do |name|
  path = File.join(COURSE, "_shared", name)
  errors << "Missing courses/project-lab/_shared/#{name}" unless File.file?(path) && !File.zero?(path)
end

level_dirs = Dir.glob(File.join(COURSE, "level-*" )).select { |path| File.directory?(path) }.sort
expected_dirs = (1..5).map { |number| File.join(COURSE, format("level-%02d", number)) }
errors << "Expected exactly Project Lab level-01 through level-05" unless level_dirs == expected_dirs

expected_dirs.each_with_index do |directory, index|
  number = index + 1
  level_name = File.basename(directory)
  REQUIRED_LEVEL_FILES.each do |name|
    path = File.join(directory, name)
    errors << "Missing courses/project-lab/#{level_name}/#{name}" unless File.file?(path) && !File.zero?(path)
  end
  REQUIRED_LEVEL_PDFS.each do |name|
    path = File.join(directory, name)
    errors << "Missing courses/project-lab/#{level_name}/#{name}" unless File.file?(path) && !File.zero?(path)
  end

  manifest_path = File.join(directory, "level.yml")
  next unless File.file?(manifest_path)

  manifest = YAML.safe_load_file(manifest_path)
  missing = MANIFEST_KEYS - manifest.keys
  errors << "#{level_name} manifest missing: #{missing.join(', ')}" unless missing.empty?
  errors << "#{level_name} has number #{manifest['number'].inspect}" unless manifest["number"] == number

  {
    "student.md" => %w[title objective passing_proof],
    "instructor.md" => %w[title objective passing_proof],
    "worksheet.md" => %w[title passing_proof],
    "slides.html" => %w[title objective passing_proof],
  }.each do |name, keys|
    path = File.join(directory, name)
    next unless File.file?(path)

    content = normalized(File.read(path))
    keys.each do |key|
      errors << "#{level_name}/#{name} does not match manifest #{key}" unless content.include?(normalized(manifest.fetch(key)))
    end
  end

  student_path = File.join(directory, "student.md")
  if File.file?(student_path)
    student = File.read(student_path)
    [
      "By the end of class", "## Anchors / Anclas", "## Safety stop / Alto de seguridad",
      "## Task 1:", "## Task 2:", "## Task 3:", "## Quick check before proof",
      "## Pass this level", "## If something fails", "## Resumen en español",
      "Builder extension",
    ].each do |marker|
      errors << "#{level_name}/student.md missing marker: #{marker}" unless student.include?(marker)
    end
  end

  instructor_path = File.join(directory, "instructor.md")
  if File.file?(instructor_path)
    instructor = File.read(instructor_path)
    [
      "## Alignment", "## Teaching stance", "## Prepare before learners arrive",
      "## Safety boundary", "## 90-minute schedule", "## Facilitation plan",
      "## Passing proof", "## Grading guide", "## Access and support",
      "## Fallbacks", "## After class",
    ].each do |marker|
      errors << "#{level_name}/instructor.md missing marker: #{marker}" unless instructor.include?(marker)
    end
    total = schedule_total(instructor_path)
    errors << "#{level_name} schedule totals #{total.inspect}, not 90" unless total == 90
  end

  worksheet_path = File.join(directory, "worksheet.md")
  if File.file?(worksheet_path)
    worksheet = File.read(worksheet_path)
    [
      "## Goal and pass check", "## Safety check / Verificación de seguridad",
      "## Task 1", "## Task 2", "## Task 3", "## Partner", "## Proof",
      "## Exit ticket",
    ].each do |marker|
      errors << "#{level_name}/worksheet.md missing marker: #{marker}" unless worksheet.include?(marker)
    end
  end

  slides_path = File.join(directory, "slides.html")
  if File.file?(slides_path)
    slides = File.read(slides_path)
    slide_tags = slides.scan(/<section\b(?=[^>]*\bclass\s*=\s*(?:"[^"]*\bslide\b[^"]*"|'[^']*\bslide\b[^']*'))[^>]*>/i)
    errors << "#{level_name}/slides.html has #{slide_tags.length} slides, expected 20" unless slide_tags.length == 20
    slide_numbers = slide_tags.filter_map { |tag| tag[/\baria-label\s*=\s*["']Slide (\d+):[^"']*["']/i, 1]&.to_i }
    errors << "#{level_name}/slides.html needs sequential Slide 1 through Slide 20 labels" unless slide_numbers == (1..20).to_a
    errors << "#{level_name}/slides.html needs tabindex=-1 on every slide" unless slide_tags.all? { |tag| tag.match?(/\btabindex\s*=\s*["']-1["']/i) }
    [
      "@media print", "aria-live=\"polite\"", "setAttribute('aria-hidden'",
      "addEventListener('keydown'", "previous.addEventListener('click'",
      "next.addEventListener('click'", ".focus({ preventScroll: true })",
      "RESUMEN EN ESPAÑOL",
    ].each do |marker|
      errors << "#{level_name}/slides.html missing accessibility or language marker: #{marker}" unless slides.include?(marker)
    end
  end

  REQUIRED_ASSETS.fetch(number).each do |name|
    path = File.join(directory, "assets", name)
    errors << "Missing courses/project-lab/#{level_name}/assets/#{name}" unless File.file?(path) && !File.zero?(path)
  end
end

course_text_files = Dir.glob(File.join(COURSE, "**", "*")).select { |path| File.file?(path) }
course_text_files.each do |path|
  next unless %w[.html .md .py .rb .template .txt .yml .yaml].include?(File.extname(path))

  relative = path.delete_prefix(ROOT + "/")
  content = File.read(path)
  errors << "#{relative} still names the retired fictional case" if content.match?(/Ocotillo Comfort/i)
end

[
  "level-01/assets/training-record-a.md",
  "level-01/assets/training-record-b.md",
  "level-04/assets/mail-desk-vulnerable.md",
  "level-04/assets/mail-desk-fixed.md",
  "level-05/assets/training-faq.md",
].each do |relative|
  path = File.join(COURSE, relative)
  next unless File.file?(path)

  errors << "#{relative} must remain visibly training-only" unless File.read(path).include?("TRAINING-ONLY")
end

if File.file?(LANDING)
  landing = File.read(LANDING)
  (1..5).each do |number|
    level = format("level-%02d", number)
    errors << "Public landing page does not link to #{level}" unless landing.include?("courses%2Fproject-lab%2F#{level}%2Fstudent.md")
  end
  errors << "Public landing page still names the twelve-level course" if landing.match?(/twelve[- ]level/i)
end

project_lab_landing = File.join(COURSE, "index.html")
if File.file?(project_lab_landing)
  landing = File.read(project_lab_landing)
  course_login = '<a class="course-login" href="https://learn.zerotoagent.org/auth/users/sign_in">Course login</a>'
  errors << "Project Lab header is missing the branded course login" unless landing.include?(course_login)
  errors << "Project Lab course login must remain visible on mobile" unless landing.include?('nav { display:none; }') && landing.include?('.course-login { position:absolute; right:20px;')
  linked_materials = landing.scan(/<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>/).select do |_href, label|
    label.match?(/Lesson|Worksheet|Instructor|Safety card|Test sheet|Access routes|Presentation rubric|Answer key/i)
  end
  linked_materials.each do |href, label|
    errors << "#{label} must link to a PDF, not #{href}" unless File.extname(href) == ".pdf"
    anchor = landing[/<a\s+href="#{Regexp.escape(href)}"[^>]*>/]
    errors << "#{label} PDF must open in a new tab" unless anchor&.include?('target="_blank"')
    errors << "#{label} PDF needs rel=noopener" unless anchor&.include?('rel="noopener"')
    errors << "#{label} points to a missing file: #{href}" unless File.file?(File.join(COURSE, href))
  end
  linked_pdf_count = landing.scan(/<a\s+href="[^"]+\.pdf"\s+target="_blank"\s+rel="noopener">/).length
  errors << "Project Lab landing page has #{linked_pdf_count} PDF links, expected 27" unless linked_pdf_count == 27
  slide_link_count = landing.scan(/<a\s+href="level-\d{2}\/slides\.html"\s+target="_blank"\s+rel="noopener">Slides<\/a>/).length
  errors << "Project Lab landing page has #{slide_link_count} new-tab slide links, expected 5" unless slide_link_count == 5
  errors << "Project Lab landing page still links to Markdown course material" if landing.match?(/<a\s+href="[^"]+\.md"/)
end

if errors.empty?
  puts "Project Lab valid: 5 levels, 90 minutes each, English complete with Spanish phase-one support."
else
  warn errors.map { |error| "ERROR: #{error}" }.join("\n")
  exit 1
end
