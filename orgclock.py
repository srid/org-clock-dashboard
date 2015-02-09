import re
import rumps
rumps.debug_mode(True)

## utilities
## ---------

def run(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True).strip()

def run_emacsclient(elisp):
    return run('emacsclient -e "%s"' % elisp)


## orgmode functions
## -----------------

org_regex = re.compile('\#\(\\"\s*(.+)\\".*')
def org_parse_clock_string(s):
    r = org_regex.search(s)
    return r.groups()[0]

def org_clock_string():
    import re
    if run_emacsclient("(org-clock-is-active)") == "nil":
        return "Org IDLE"
    else:
        # TODO: parse this string
        # TODO: set icon accordingly
        s = run_emacsclient("(org-clock-get-clock-string)").splitlines()[0]
        s = org_parse_clock_string(s)
        return s

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
        print sender
        app.title = org_clock_string()
    # XXX: running emacsclient every two seconds; may not be a good
    # idea.
    timer = rumps.Timer(timer_func, 2)

    # TODO: check emacs install before starting app.
    timer.start()
    app.run()
