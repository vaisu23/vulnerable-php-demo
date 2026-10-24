<?php

declare(strict_types=1);

namespace Demo\DependencyFixCrewTarget;

final class App
{
    public function render(): string
    {
        $runtime = htmlspecialchars(PHP_VERSION, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

        return "<!doctype html>\n" .
            "<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Dependency Fix Crew PHP Demo</title></head>\n" .
            "<body><main><h1>Dependency Fix Crew PHP Demo</h1>\n" .
            "<p>Runtime PHP version: <strong>{$runtime}</strong></p>\n" .
            "<p>This minimal application is a dependency scanner test target.</p></main></body></html>\n";
    }
}
