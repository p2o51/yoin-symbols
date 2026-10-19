import com.vanniktech.maven.publish.AndroidSingleVariantLibrary
import com.vanniktech.maven.publish.JavadocJar
import com.vanniktech.maven.publish.SourcesJar

plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.maven.publish)
}

// Also set on the project so an app's includeBuild() substitutes io.github.p2o51:yoin-symbols.
group = providers.gradleProperty("GROUP").get()
version = providers.gradleProperty("VERSION_NAME").get()

android {
    namespace = "com.gpo.yoin.symbols"
    compileSdk = 36

    defaultConfig {
        minSdk = 23
    }

    resourcePrefix = "ic_yoin_"

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    api(platform(libs.compose.bom))
    api(libs.compose.runtime)
    api(libs.compose.ui)
    api(libs.compose.ui.graphics)
    api(libs.compose.animation.core)
}

// Credentials never live in the repo. Set them in ~/.gradle/gradle.properties or as
// ORG_GRADLE_PROJECT_* environment variables: mavenCentralUsername, mavenCentralPassword
// (a Central Portal user token), signingInMemoryKey, signingInMemoryKeyId,
// signingInMemoryKeyPassword. See RELEASING.md.
mavenPublishing {
    // Uploads only; the deployment is published by hand on central.sonatype.com.
    publishToMavenCentral()
    // Without a key (CI checks, publishToMavenLocal) the artifacts stay unsigned;
    // the Central Portal rejects an unsigned deployment, so nothing slips through.
    if (providers.gradleProperty("signingInMemoryKey").isPresent) {
        signAllPublications()
    }

    coordinates(
        groupId = group.toString(),
        artifactId = "yoin-symbols",
        version = version.toString(),
    )

    configure(
        AndroidSingleVariantLibrary(
            // Maven Central wants a javadoc jar; the KDoc lives in the sources jar.
            javadocJar = JavadocJar.Empty(),
            sourcesJar = SourcesJar.Sources(),
            variant = "release",
        ),
    )

    pom {
        name.set("Yoin Symbols")
        description.set(
            "Light, rounded line icons with continuous-curvature containers for Jetpack Compose, " +
                "plus spring-animated symbols.",
        )
        inceptionYear.set("2026")
        url.set("https://github.com/p2o51/yoin-symbols")
        licenses {
            license {
                name.set("MIT License")
                url.set("https://opensource.org/licenses/MIT")
                distribution.set("repo")
            }
        }
        developers {
            developer {
                id.set("p2o51")
                name.set("p2o51")
                url.set("https://github.com/p2o51")
            }
        }
        scm {
            url.set("https://github.com/p2o51/yoin-symbols")
            connection.set("scm:git:https://github.com/p2o51/yoin-symbols.git")
            developerConnection.set("scm:git:ssh://git@github.com/p2o51/yoin-symbols.git")
        }
    }
}
