pluginManagement {
    repositories {
        google {
            content {
                includeGroupByRegex("com\\.android.*")
                includeGroupByRegex("com\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "yoin-symbols-android"

// The project name is the Maven artifactId, so an app that does
// includeBuild("../yoin-symbols/android") gets io.github.p2o51:yoin-symbols
// substituted with this source automatically.
include(":yoin-symbols")
