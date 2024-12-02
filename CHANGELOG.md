## Version 0.5.2 (2024/12/02)


### Pull Requests Merged

#### Features added

* [PR 75](https://github.com/pytroll/trollsift/pull/75) - Switch to pyproject.toml

In this release 1 pull request was closed.


## Version 0.5.1 (2023/10/09)


### Pull Requests Merged

#### Bugs fixed

* [PR 49](https://github.com/pytroll/trollsift/pull/49) - Update versioneer to stop using deprecated distutils module.

#### Features added

* [PR 56](https://github.com/pytroll/trollsift/pull/56) - Add readthedocs configuration file

In this release 2 pull requests were closed.


## Version 0.5.0 (2022/11/21)

### Issues Closed

* [Issue 45](https://github.com/pytroll/trollsift/issues/45) - Provide simple access to defined keys of a parser instance ([PR 46](https://github.com/pytroll/trollsift/pull/46) by [@carloshorn](https://github.com/carloshorn))
* [Issue 37](https://github.com/pytroll/trollsift/issues/37) - Global instances of formatters ([PR 38](https://github.com/pytroll/trollsift/pull/38) by [@Regan-Koopmans](https://github.com/Regan-Koopmans))
* [Issue 36](https://github.com/pytroll/trollsift/issues/36) - Alignment marker is not optional for numbers when it should
* [Issue 34](https://github.com/pytroll/trollsift/issues/34) - Trollsift doesn't parse hex numbers ([PR 35](https://github.com/pytroll/trollsift/pull/35) by [@mraspaud](https://github.com/mraspaud))

In this release 4 issues were closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 38](https://github.com/pytroll/trollsift/pull/38) - Replace global RegexFormatter with memoized function ([37](https://github.com/pytroll/trollsift/issues/37))
* [PR 35](https://github.com/pytroll/trollsift/pull/35) - Add hex, octal, and binary parsing ([34](https://github.com/pytroll/trollsift/issues/34))

#### Features added

* [PR 46](https://github.com/pytroll/trollsift/pull/46) - Add keys method to Parser class ([45](https://github.com/pytroll/trollsift/issues/45))

In this release 3 pull requests were closed.


## Version 0.4.0 (2022/02/03)

### Issues Closed

* [Issue 30](https://github.com/pytroll/trollsift/issues/30) - Problems with padding syntax ([PR 33](https://github.com/pytroll/trollsift/pull/33) by [@paulovcmedeiros](https://github.com/paulovcmedeiros))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 33](https://github.com/pytroll/trollsift/pull/33) - Fix problems with type='' in string padding syntax ([30](https://github.com/pytroll/trollsift/issues/30))

#### Features added

* [PR 32](https://github.com/pytroll/trollsift/pull/32) - Add 'allow_partial' keyword to compose
* [PR 31](https://github.com/pytroll/trollsift/pull/31) - Change tested Python versions to 3.8, 3.9 and 3.10
* [PR 24](https://github.com/pytroll/trollsift/pull/24) - Skip Python2 support and require python 3.6 or higher


## Version 0.3.5 (2021/02/15)

### Issues Closed

* [Issue 27](https://github.com/pytroll/trollsift/issues/27) - Parsing zero padded floats
* [Issue 26](https://github.com/pytroll/trollsift/issues/26) - MNT: Stop using ci-helpers in appveyor.yml
* [Issue 23](https://github.com/pytroll/trollsift/issues/23) - Bug when parsing leap day when you dont have year
* [Issue 20](https://github.com/pytroll/trollsift/issues/20) - Special conversion specifiers do not work ([PR 21](https://github.com/pytroll/trollsift/pull/21))

In this release 4 issues were closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 21](https://github.com/pytroll/trollsift/pull/21) - Fix typo in string formatting usage example and drop Python 2.7 tests ([20](https://github.com/pytroll/trollsift/issues/20))

#### Features added

* [PR 29](https://github.com/pytroll/trollsift/pull/29) - GitHub actions
* [PR 25](https://github.com/pytroll/trollsift/pull/25) - Add lru_cache to parsing for improved performance

In this release 3 pull requests were closed.


## Version 0.3.4 (2019/12/18)

### Issues Closed

* [Issue 18](https://github.com/pytroll/trollsift/issues/18) - Different parsing allignment behaviour between 0.2.* and 0.3.* ([PR 19](https://github.com/pytroll/trollsift/pull/19))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 19](https://github.com/pytroll/trollsift/pull/19) - Fix regex parser being too greedy with partial string patterns ([18](https://github.com/pytroll/trollsift/issues/18))

In this release 1 pull request was closed.


## Version 0.3.3 (2019/10/09)

### Pull Requests Merged

#### Bugs fixed

* [PR 15](https://github.com/pytroll/trollsift/pull/15) - Fix parse accepting strings with trailing characters

#### Features added

* [PR 14](https://github.com/pytroll/trollsift/pull/14) - Adding .stickler.yml configuration file

In this release 2 pull requests were closed.


## Version 0.3.2 (2019/01/14)


### Pull Requests Merged

#### Bugs fixed

* [PR 13](https://github.com/pytroll/trollsift/pull/13) - Fix backslashes in regex patterns on Windows

In this release 1 pull request was closed.


## Version 0.3.1 (2018/11/02)

### Issues Closed

* [Issue 11](https://github.com/pytroll/trollsift/issues/11) - Using the same information in two places in the template is fails with 0.3.0 ([PR 12](https://github.com/pytroll/trollsift/pull/12))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 12](https://github.com/pytroll/trollsift/pull/12) - Fix fields being specified multiple times in one pattern ([11](https://github.com/pytroll/trollsift/issues/11))

In this release 1 pull request was closed.

## Version 0.3.0 (2018/09/29)

### Issues Closed

* [Issue 5](https://github.com/pytroll/trollsift/issues/5) - Add custom string formatter for lower/upper support

In this release 1 issue was closed.

### Pull Requests Merged

#### Features added

* [PR 6](https://github.com/pytroll/trollsift/pull/6) - Add additional string formatting conversion options

In this release 1 pull request was closed.


## Version 0.2.1 (2018/05/22)

### Issues Closed

* [Issue 3](https://github.com/pytroll/trollsift/issues/3) - Packaging license file ([PR 4](https://github.com/pytroll/trollsift/pull/4))

In this release 1 issues were closed.

### Pull Requests Merged

#### Features added

* [PR 4](https://github.com/pytroll/trollsift/pull/4) - Update travis tests and add appveyor tests ([3](https://github.com/pytroll/trollsift/issues/3))

In this release 1 pull request was closed.


## Version 0.2.0 (2017/12/08)

### Issues Closed

* [Issue 2](https://github.com/pytroll/trollsift/issues/2) - Another timestring issue
* [Issue 1](https://github.com/pytroll/trollsift/issues/1) - problem when parsing time strings

In this release 2 issues were closed.
