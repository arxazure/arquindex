<?php
declare(strict_types=1);

const SOURCE_ORIGIN = 'https://arquindex-gestao-documental.arquindex.chatgpt.site';
const BASE_PATH = '/gestao-documental';
const CANONICAL_BASE = 'https://www.arquindex.com.br/gestao-documental';
const INDEXNOW_KEY = 'a948be82c7824bc989f2c5dd0f071bea';

$path = parse_url($_SERVER['REQUEST_URI'] ?? BASE_PATH . '/', PHP_URL_PATH) ?: BASE_PATH . '/';
if ($path === BASE_PATH . '/_health') {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok' => true, 'service' => 'arquindex-homehost-replica'], JSON_UNESCAPED_SLASHES);
    exit;
}
if ($path === BASE_PATH . '/' . INDEXNOW_KEY . '.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    echo INDEXNOW_KEY;
    exit;
}
if (strpos($path, BASE_PATH) !== 0) {
    http_response_code(404);
    exit;
}
$upstreamPath = substr($path, strlen(BASE_PATH)) ?: '/';
$query = $_SERVER['QUERY_STRING'] ?? '';
$url = SOURCE_ORIGIN . $upstreamPath . ($query !== '' ? '?' . $query : '');

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_MAXREDIRS => 4,
    CURLOPT_CONNECTTIMEOUT => 10,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_USERAGENT => $_SERVER['HTTP_USER_AGENT'] ?? 'ArquindexReplica/1.0',
    CURLOPT_ENCODING => '',
]);
$body = curl_exec($ch);
$status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
$contentType = (string) (curl_getinfo($ch, CURLINFO_CONTENT_TYPE) ?: 'application/octet-stream');
$error = curl_error($ch);
curl_close($ch);

if ($body === false || $status < 100) {
    http_response_code(502);
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: no-store');
    echo '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Arquindex</title><h1>Conteúdo temporariamente indisponível</h1><p>Acesse o <a href="/">site principal da Arquindex</a> ou fale pelo <a href="https://wa.me/5531973632725">WhatsApp</a>.</p></html>';
    exit;
}

$textTypes = ['text/', 'application/xml', 'application/json', 'application/javascript', 'image/svg+xml'];
$isText = false;
foreach ($textTypes as $prefix) if (strpos($contentType, $prefix) !== false) $isText = true;

if ($isText) {
    $marker = '__ARQUINDEX_REPLICA_CANONICAL_BASE__';
    $body = str_replace(SOURCE_ORIGIN . '/', $marker, $body);
    $body = str_replace(SOURCE_ORIGIN, CANONICAL_BASE, $body);
    $prefixes = [
        '_next','api','autores','blog','brasil','cidades','comparativo','conhecimento',
        'feed.xml','favicon.svg','glossario','llms-full.txt','llms.txt','manifest.webmanifest',
        'orcamento','privacidade','robots.txt','setores','sitemap','solucoes',
        'a948be82c7824bc989f2c5dd0f071bea.txt'
    ];
    foreach ($prefixes as $prefix) $body = str_replace('/' . $prefix, BASE_PATH . '/' . $prefix, $body);
    $body = preg_replace('/((?:href|src|action)=["\'])\/(?!\/)/i', '$1' . BASE_PATH . '/', $body);
    $body = str_replace('codex-preview" content="development', 'codex-preview" content="production', $body);
    $body = str_replace($marker, CANONICAL_BASE . '/', $body);
}

http_response_code($status);
header('Content-Type: ' . $contentType);
header('Cache-Control: ' . ($isText ? 'public, max-age=300' : 'public, max-age=86400'));
header('X-Robots-Tag: index, follow, max-snippet:-1, max-image-preview:large');
header('X-Arquindex-Replica: chatgpt-sites');
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'HEAD') echo $body;
