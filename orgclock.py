import re
import rumps
# rumps.debug_mode(True)


## utilities
## ---------

def run(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True).strip()

def run_emacsclient(elisp):
    s = run('emacsclient -e "%s"' % elisp)
    # print '>>> %s ==> %s' % (elisp, s)
    return s

## orgmode functions
## -----------------

org_regex = re.compile('\#\(\"\s*\[(.+)/(.+)\] \((.+)\)\".*')
def org_parse_clock_string(s):
    r = org_regex.search(s)
    return r.groups()

def org_clock_string():
    # TODO: set icon accordingly
    if run_emacsclient("(org-clock-is-active)") == "nil":
        return None
    else:
        s = run_emacsclient("(org-clock-get-clock-string)").splitlines()[0]
        elapsed, estimated, title = org_parse_clock_string(s)
        return "%s -- %s" % (elapsed, title)

def org_goto_clock():
    import subprocess
    cmd = 'emacsclient -e "(call-interactively \'org-clock-goto)"'
    subprocess.check_call(cmd, shell=True)
    subprocess.check_call(["open", "-a", "Emacs"]) # activate Emacs window


## osx menubar app
## ---------------

class OrgClockStatusBarApp(rumps.App):
    @rumps.clicked("Go to current/recent task")
    def current_task(self, _):
        org_goto_clock()

    @rumps.clicked("Refresh")
    def sayhi(self, _):
        clock_title = org_clock_string()
        self.title = clock_title

        
if __name__ == "__main__":
    app = OrgClockStatusBarApp("Org clock")
    def timer_func(sender):
        s = org_clock_string()
        print s  # removing the print statement makes the app hang.
        if s is not None:
            app.title = s
        else:
            app.title = "Not tracking"

    timer = rumps.Timer(timer_func, 5)

    # TODO: check emacs install before starting app.
    timer.start()
    app.icon = "task.png"
    app.run()
