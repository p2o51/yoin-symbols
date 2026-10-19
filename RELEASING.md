# Releasing

One version number, in `VERSION`, is shared by every package. Pushing a tag `vX.Y.Z` publishes all of them.

## Every release

1. Update `VERSION` and add a section to `CHANGELOG.md`.
2. Regenerate: `python3 generator/build.py` (this also writes the version into `android/gradle.properties`, `web/package.json` and `flutter/pubspec.yaml`).
3. Commit, then tag and push:

   ```sh
   git tag vX.Y.Z
   git push origin main vX.Y.Z
   ```

The [release workflow](.github/workflows/release.yml) checks that the tag matches `VERSION`, then uploads to Maven Central, publishes to npm and pub.dev, and creates a GitHub release with the SVGs and fonts attached. The gallery on GitHub Pages updates from `docs/` on `main`.

The Maven Central upload is not released automatically. When the `maven` job is green, open [Deployments](https://central.sonatype.com/publishing/deployments), check the files of the `io.github.p2o51:yoin-symbols` deployment, and press **Publish**. It reaches `repo1.maven.org` within about half an hour; search may take longer. Releases on Maven Central cannot be deleted.

## One-time setup

### Maven Central

1. Sign in at [central.sonatype.com](https://central.sonatype.com) with GitHub. The namespace `io.github.p2o51` is verified automatically for that account.
2. Generate a user token at [central.sonatype.com/usertoken](https://central.sonatype.com/usertoken) → Generate User Token. The modal shows a username and a password once; copy both.
3. Create a signing key and publish its public half:

   ```sh
   gpg --full-generate-key                       # RSA and RSA, 4096 bits
   gpg --list-secret-keys --keyid-format=long     # note the key id
   gpg --keyserver keyserver.ubuntu.com --send-keys <KEY_ID>
   gpg --armor --export-secret-keys <KEY_ID>      # goes into SIGNING_KEY / signingInMemoryKey
   ```

4. Add repository secrets (Settings → Secrets and variables → Actions):

   | Secret | Value |
   | --- | --- |
   | `CENTRAL_TOKEN_USERNAME` | user token name |
   | `CENTRAL_TOKEN_PASSWORD` | user token password |
   | `SIGNING_KEY` | the ASCII-armoured private key |
   | `SIGNING_KEY_PASSWORD` | its passphrase |

The [Gradle maven-publish plugin](https://vanniktech.github.io/gradle-maven-publish-plugin/central/) signs the artifacts and uploads them with `publishToMavenCentral`, which leaves the deployment for a manual Publish.

To upload from your own machine instead, put the same values in `~/.gradle/gradle.properties` (never in the repo):

```properties
mavenCentralUsername=<user token username>
mavenCentralPassword=<user token password>
signingInMemoryKeyId=<last 8 hex digits of the key id>
signingInMemoryKeyPassword=<passphrase>
signingInMemoryKey=<the armoured private key, newlines written as \n>
```

then run `cd android && ./gradlew :yoin-symbols:publishToMavenCentral`.

### npm

1. Publish the first version by hand, which creates the package:

   ```sh
   cd web && npm login && npm publish --access public
   ```

2. On npmjs.com, open the package settings → Trusted Publisher → GitHub Actions: repository `p2o51/yoin-symbols`, workflow `release.yml`.

After that the workflow publishes without a token, with provenance.

### pub.dev

1. Publish the first version by hand: `cd flutter && flutter pub publish`.
2. On pub.dev, open the package admin page → Automated publishing → enable publishing from GitHub Actions for `p2o51/yoin-symbols` with the tag pattern `v{{version}}`.

### GitHub Pages

Settings → Pages → Deploy from a branch → `main`, folder `/docs`.

### Figma

In the [Figma file](https://www.figma.com/design/g0H4CfkagF8p1N4vuPYxQA): Share → set “Anyone with the link” to view so the README link works. Assets → Publish makes it a team library; Share → Publish to Community puts it on Figma Community.

## Local builds without publishing

```sh
cd android && ./gradlew :yoin-symbols:publishToMavenLocal   # ~/.m2, unsigned unless a key is set
cd web && npm pack                                         # yoin-symbols-X.Y.Z.tgz
cd flutter && flutter pub publish --dry-run
```
