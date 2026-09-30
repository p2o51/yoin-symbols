plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.compose)
    `maven-publish`
    signing
}

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

    publishing {
        singleVariant("release") {
            withSourcesJar()
        }
    }
}

dependencies {
    api(platform(libs.compose.bom))
    api(libs.compose.runtime)
    api(libs.compose.ui)
    api(libs.compose.ui.graphics)
    api(libs.compose.animation.core)
}

// Maven Central wants a javadoc jar; the KDoc lives in the sources jar.
val emptyJavadocJar by tasks.registering(Jar::class) {
    archiveClassifier.set("javadoc")
}

publishing {
    publications {
        register<MavenPublication>("release") {
            groupId = project.group.toString()
            artifactId = "yoin-symbols"
            version = project.version.toString()
            artifact(emptyJavadocJar)
            afterEvaluate {
                from(components["release"])
            }
            pom {
                name.set("Yoin Symbols")
                description.set(
                    "Light, rounded line icons with continuous-curvature containers for Jetpack Compose, " +
                        "plus spring-animated symbols.",
                )
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
    }
    repositories {
        // Release workflow zips this folder and uploads it to the Maven Central Portal.
        maven {
            name = "staging"
            url = uri(layout.buildDirectory.dir("staging-deploy"))
        }
    }
}

signing {
    val signingKey = providers.gradleProperty("signingInMemoryKey").orNull
    if (signingKey != null) {
        useInMemoryPgpKeys(signingKey, providers.gradleProperty("signingInMemoryKeyPassword").orNull)
        sign(publishing.publications)
    }
}
