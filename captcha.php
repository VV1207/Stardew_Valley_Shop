<?php
if (session_status() === PHP_SESSION_NONE) {
    session_set_cookie_params(0, '/');
    session_start();
}

// 生成随机验证码
$captcha_code = '';
$chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz';
for ($i = 0; $i < 4; $i++) {
    $captcha_code .= $chars[random_int(0, strlen($chars) - 1)];
}

// 存储到 session
$_SESSION['captcha'] = $captcha_code;

// 创建图片
$width = 120;
$height = 40;
$image = imagecreatetruecolor($width, $height);

// 背景色
$bg_color = imagecolorallocate($image, 250, 248, 240);
imagefill($image, 0, 0, $bg_color);

// 绘制干扰线
for ($i = 0; $i < 5; $i++) {
    $line_color = imagecolorallocate($image, random_int(150, 220), random_int(150, 220), random_int(150, 220));
    imageline($image, random_int(0, $width), random_int(0, $height), random_int(0, $width), random_int(0, $height), $line_color);
}

// 绘制干扰点
for ($i = 0; $i < 30; $i++) {
    $dot_color = imagecolorallocate($image, random_int(150, 230), random_int(150, 230), random_int(150, 230));
    imagesetpixel($image, random_int(0, $width), random_int(0, $height), $dot_color);
}

// 绘制验证码文字（使用内置字体）
$text_colors = [
    imagecolorallocate($image, 61, 104, 48),   // 绿色
    imagecolorallocate($image, 197, 127, 30),   // 橙色
    imagecolorallocate($image, 87, 139, 52),    // 深绿
    imagecolorallocate($image, 107, 94, 74),    // 棕色
];

for ($i = 0; $i < strlen($captcha_code); $i++) {
    $color = $text_colors[$i % count($text_colors)];
    $angle = random_int(-15, 15);
    $x = 10 + $i * 26;
    $y = random_int(25, 35);
    imagestring($image, 5, $x, $y - 15, $captcha_code[$i], $color);
}

// 边框
$border_color = imagecolorallocate($image, 212, 200, 170);
imagerectangle($image, 0, 0, $width - 1, $height - 1, $border_color);

// 输出图片
header('Content-Type: image/png');
header('Cache-Control: no-cache, no-store, must-revalidate');
imagepng($image);
imagedestroy($image);
?>