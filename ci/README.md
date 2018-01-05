# Continuous Integration w/ Jenkins
> This folder contains a config file that can be used for setting up a local Jenkins job

This project works well with [Jenkins](https://jenkins.io/) as a continuous integration server. If you don't have it already, the fastest method on OSX is with the brew tool using the command `brew install jenkins`.

You can then start Jenkins up with the command `brew services start jenkins` or `jenkins`.

Note: You will need to run `jenkins` at least one time to set it up after the install.

Now browse to <http://localhost:8080> and follow the instructions to complete the installation.

You're now ready to create or (take the easy route and) install the provided example job. The folder inside of the jobs folder will need to be copied over to your local `~/.jenkins/jobs` folder eventually. But first, the config file should be updated to match your personal system settings.

## config.xml
In the config.xml you will find all of the properties of a Jenkins job. Before moving the parent folder (`littlebenchmark-local-prod`) over to your Jenkins path (usually at `~/.jenkins/jobs`), there are a few lines you should change. You can find these by searching the file for the following items.

|| Variable || Description ||
|| -------- || ----------- ||
| PATH_TO_CLONED_GIT_PROJECT | This is essentially the project files that you cloned from Github. You'll need to include a path like this `/Users/robsawyer/Sites/lb/.git`. |
| AUTH_TOKEN_FOR_USER | A custom token/password for the SCM build trigger. |
| NOTIFICATION_EMAIL_ADDRESS | This email address will be notified based on the job email settings. |
| credentialsId | Not sure if you'll need to replace this, but maybe. |

# Build after commit
In order for Jenkins to build after a commit, you will need to add a `post-commit` hook inside your local repo's `.git` folder. Add the file `post-commit` under the `.git/hooks/` folder and use the following to get started.

```
#!/bin/bash

echo "Pinging Jenkins..."

# The url to a Jenkins instance
JENKINS_URL=http://localhost:8080

# Create a Jenkins user and this will become obvious
API_TOKEN=[SOME_TOKEN]

# Your jenkins job name. If you're using the config above, leave this as is.
JOB_NAME=littlebenchmark-local-prod

# Should match the token you added above for the SCM build trigger
TOKEN=[AUTH_TOKEN_FOR_USER]

# The user you created to manage Jenkins builds
USER=[USERNAME]

# The path to the local Github repo
CLONE_PATH=[~/Sites/lb]

# TODO: Figure out how to get this working
# Read more here: https://github.com/jan-molak/jenkins-build-monitor-plugin/issues/215
# And see crumb updates: https://github.com/jenkinsci/jenkins/compare/4649e04cbe58...a87c38c5052c
# More related stuff: https://issues.jenkins-ci.org/browse/JENKINS-12875
# CRUMB=$(curl --user $USER:$API_TOKEN ${JENKINS_URL}/crumbIssuer/api/xml?xpath=concat\(//crumbRequestField,":",//crumb\))

# Fire the curl command to trigger the build
curl -X POST --user $USER:$API_TOKEN $JENKINS_URL/job/$JOB_NAME/build?token=$TOKEN >> $CLONE_PATH/logs/git-post-commit-results.log

```

If it worked, you'll see something similar to the following during a commit.
```
$ git commit -am "README updates"
Pinging Jenkins...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
[master 1bb38cc] README updates
 1 file changed, 39 insertions(+), 1 deletion(-)
```

# Email Notifications
In order to send emails locally, you'll need to ensure your local SMTP email client is configured properly. If you don't know what I'm talking about, check out [How to send emails from localhost (MAC OS X El Capitan)](http://www.developerfiles.com/how-to-send-emails-from-localhost-mac-os-x-el-capitan/).

> Make sure postfix is running with `sudo postfix start`

# Break something?
If something breaks, read the Jenkins documentation file named [Moving/copying/renaming Jenkins jobs](https://wiki.jenkins-ci.org/display/JENKINS/Administering+Jenkins#AdministeringJenkins-Moving%2Fcopying%2Frenamingjobs) for more.

# Gotchas
The newish CSRF protection feature is a real pain when working locally. To disable it and live on the edge, visit [Remote access API](https://wiki.jenkins-ci.org/display/JENKINS/Remote+access+API#RemoteaccessAPI-CSRFProtection).

# Resources
- [Installing Jenkins OS X Homebrew](http://flummox-engineering.blogspot.com/2016/01/installing-jenkins-os-x-homebrew.html)
- [Using Tox with the Jenkins Integration Server](http://tox.readthedocs.io/en/latest/example/jenkins.html)
- [How to configure Git post commit hook](http://stackoverflow.com/questions/12794568/how-to-configure-git-post-commit-hook)
