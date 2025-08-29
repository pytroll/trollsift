# Releasing trollsift

1. checkout main branch
2. pull from repo
3. run the unittests
4. run `loghub` and update the `CHANGELOG.md` file:

   ```
   loghub pytroll/trollsift --token $LOGHUB_GITHUB_TOKEN -st $(git tag --sort=-version:refname --list 'v*' | head -n 1) -plg bug "Bugs fixed" -plg enhancement "Features added" -plg documentation "Documentation changes" -plg backwards-incompatibility "Backwards incompatible changes"
   ```

   Don't forget to commit!

5. Create a tag with the new version number, starting with a 'v', eg:

   ```
   git tag -a v0.22.45 -m "Version 0.22.45"
   ```

   See [semver.org](http://semver.org/) on how to write a version number.

6. push changes to github `git push --follow-tags`
7. Verify tests pass on GitHub Actions
8. Create a "Release" on GitHub by going to
   https://github.com/pytroll/pyresample/releases and clicking "Draft a new release".
   On the next page enter the newly created tag in the "Tag version" field,
   "Version X.Y.Z" in the "Release title" field, and paste the markdown from
   the changelog (the portion under the version section header) in the
   "Describe this release" box. Finally click "Publish release".
9. Verify the GitHub actions for deployment succeed and the release is on PyPI.
