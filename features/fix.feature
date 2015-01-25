Feature: Reset fixit branch to commit ref
  In order to groom a mid-branch commit
  As a developer using Git
  I need a way to safely checkout an arbitrary commit with a working ref


  @wip
  Scenario: Checkout existing fixit at new commit
    Given the working directory is a Git repo
      And the current branch is 'spike'
     When I issue the command `fix 28f1215`
     Then the current branch is 'fixit'
      And HEAD is 28f1215


  @wip
  @linear-repo
  Scenario: Checkout new fixit at specified commit
    Given the working directory is a Git repo
     When I issue the command `fix 1985579`
     Then the current branch is 'fixit'
      And HEAD is 1985579


  @wip
  Scenario: Reset checked-out fixit to new commit
    Given the working directory is a Git repo
      And the current branch is 'fixit'
     When I issue the command `fix 28f1215`
     Then the current branch is 'fixit'
      And HEAD is 28f1215


  @wip
  Scenario: Graceful exit when not in Git repository
    Given the working directory is not in a Git repository
     When I issue the command `fix 28f1215`
     Then the return code is 2
      And stderr output starts with 'Not in a Git repository.'
