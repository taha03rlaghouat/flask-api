<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

$pdo = new PDO("mysql:host=sql213.infinityfree.com;dbname=if0_38641180_udemy_db;charset=utf8", "if0_38641180", "Jo9hWNjcxFiZf");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$stmt = $pdo->query("SELECT lemma, translation, pronunciation FROM tokens WHERE translation IS NOT NULL AND pronunciation IS NOT NULL");
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

// 1. إنشاء محتوى LaTeX
$latex = <<<LATEX
\\documentclass[12pt]{article}
\\usepackage{fontspec}
\\usepackage[arabic,english]{babel}
\\usepackage{geometry}
\\geometry{a4paper, margin=2cm}
\\setmainfont{Charis SIL}
\\newfontfamily\\arabicfont[Script=Arabic]{Amiri}
\\usepackage{longtable}

\\begin{document}
\\begin{center}
\\section*{📚 قائمة الكلمات المترجمة}
\\begin{longtable}{|c|>{\\arabicfont}c|c|}
\\hline
\\textbf{Lemma} & \\textbf{الترجمة} & \\textbf{النطق} \\\\
\\hline
LATEX;

foreach ($rows as $row) {
    $lemma = htmlspecialchars($row['lemma']);
    $translation = htmlspecialchars($row['translation']);
    $pron = htmlspecialchars($row['pronunciation']);
    $latex .= "$lemma & $translation & $pron \\\\\n\\hline\n";
}

$latex .= <<<LATEX
\\end{longtable}
\\end{center}
\\end{document}
LATEX;

// 2. حفظ الملف
$dir = __DIR__ . '/generated';
if (!is_dir($dir)) mkdir($dir);

$texFile = $dir . '/vocab_export.tex';
file_put_contents($texFile, $latex);

// 3. توليد PDF باستخدام xelatex
chdir($dir);
exec("xelatex -interaction=nonstopmode vocab_export.tex");

// 4. عرض الملف أو تنزيله
$pdfFile = $dir . '/vocab_export.pdf';
if (file_exists($pdfFile)) {
    header('Content-Type: application/pdf');
    header('Content-Disposition: inline; filename="vocab_export.pdf"');
    readfile($pdfFile);
} else {
    echo "❌ فشل توليد الملف PDF.";
}
?>
