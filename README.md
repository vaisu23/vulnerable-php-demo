# Dependency Fix Crew PHP test target

A small, safe PHP application for exercising repository dependency and runtime-version scanning. It has no database, secrets, or intentionally vulnerable routes.

## Fixture configuration

The primary runtime is **PHP 8.3.31**. The Dockerfile pins `php:8.3.31-cli`; `.php-version` repeats that exact version. `composer.json` sets a compatible PHP constraint (`>=8.3.31 <8.4`) and requires the ordinary `psr/log` package. The lock fixture records `psr/log` 3.0.2 as an installed package.

PHP's official security advisory dated 21 October 2026 says PHP 8.3.36 fixes CVE-2026-109618 and CVE-2026-109619, and recommends updating PHP 8.3 users to 8.3.36. Therefore 8.3.31 is an affected-version test candidate relative to that same-branch fixed version. This is a runtime advisory fixture; no Composer package vulnerability is asserted. Sources: <https://www.php.net/index.php> (21 Oct 2026 advisory) and <https://www.php.net/releases/8_3_36.php>.

## Files the scanner should read

- `Dockerfile`: explicit PHP base image version, expected to take precedence.
- `.php-version`: repeated exact version for version-file detection.
- `composer.json`: project metadata and a PHP compatibility constraint.
- `composer.lock`: exact installed versions in `packages` and `packages-dev`.

All PHP version declarations are consistent. The exact runtime is 8.3.31; the Composer requirement is a range and is not itself an exact installed runtime.

## Current Dependency Fix Crew compatibility status

The public `main` branch inspected while preparing this fixture does **not** yet implement the behavior described in the task brief. In `agents/scanner.py`, the handler returns `ScanResult(ok=False, error="not implemented")` for non-mock requests, and comments mark both `kind == "version"` and `kind == "repo"` as TODO. There is no `detect_php_version()` function in that file. In `agents/advisory.py`, the handler likewise returns `AdvisoryResult(ok=False, error="not implemented")`; loading the JSON and comparing fixed versions are TODOs, and there is no `check_php_version()` function.

The existing `agents/models.py` does define the contract shape: `ScanRequest(session_id, kind, target)`, `ScanResult(session_id, ok, error, php_version, packages, source)`, `AdvisoryRequest(session_id, php_version, packages)`, and `AdvisoryResult(session_id, ok, error, findings)`. It cannot currently produce scanner or advisory results for this repository except through mock mode. This fixture is prepared to match the file formats and stated intended scanner behavior, but actual GitHub repository scanning and advisory-agent execution cannot be verified against current `main`.

The advisory's branch-specific fixed versions from `data/advisories.json` are 8.5.12, 8.4.27, 8.3.36, and 8.2.35. A valid implementation should compare 8.3.31 with the 8.3.36 entry for the same branch. PHP versions below 8.2 fall under the data's EOL note and should be distinguished from an explicit branch fixed-version match. Official PHP's advisory also notes that PHP 8.1 and older no longer receive upstream updates, and that vendor backports may exist.

## Test matrix

| Case | Fixture/input | Expected structural/advisory interpretation |
|---|---|---|
| Affected PHP | Primary target, PHP 8.3.31 | Affected relative to official PHP 8.3.36 fix |
| Fixed PHP | PHP 8.3.36 | Not affected by these two advisories on branch 8.3 |
| Newer PHP | PHP 8.3.37 | Not affected by these two advisories on branch 8.3 |
| Missing/ambiguous version | Remove Dockerfile pin and `.php-version`; only `composer.json` range remains | No exact version; scanner should report missing/ambiguous rather than guessing |
| Dependency extraction | `composer.lock` | Extract `psr/log: 3.0.2` from `packages`; `packages-dev` is present and empty |

The affected/fixed/newer verdicts are based on the official PHP advisory. The fixture tests JSON structure and a representative explicit Dockerfile tag; it does not emulate the crew scanner. The repository URL form after publishing should be `https://github.com/<owner>/vulnerable-php-demo`.

## Run locally

With PHP installed:

```sh
php -S 127.0.0.1:8080 -t public
```

Then open <http://127.0.0.1:8080>. The page displays the actual runtime `PHP_VERSION`.

Run the local structural check with Python 3:

```sh
python tests/validate_fixture.py
```

To regenerate and validate the lock file with Composer (Composer was not available in the build environment):

```sh
composer update --no-interaction
composer validate --strict
```

After the crew implements repository scanning, send the GitHub repository URL with `kind="repo"` to its existing `ScanRequest` shape, then pass returned `php_version` and `packages` into `AdvisoryRequest`. The current public implementation cannot complete these steps yet. Basic fixture validation requires no GitHub token.

A clean result for these two PHP advisories does not establish that the application or its environment is completely secure.
