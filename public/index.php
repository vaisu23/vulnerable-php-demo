<?php

declare(strict_types=1);

require dirname(__DIR__) . '/src/App.php';

use Demo\DependencyFixCrewTarget\App;

header('Content-Type: text/html; charset=utf-8');
echo (new App())->render();
