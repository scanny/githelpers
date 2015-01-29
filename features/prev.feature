Feature: Move current branch "downward" to parent commit
  In order to incrementally traverse a commit history
  As a developer using Git
  I need a way to move the current branch downward, one commit at a time


  @wip
  Scenario: Move current branch down one commit
    Given the working directory is a Git repo
      And the current branch is 'fixit'
     When I issue the command `prev`
     Then the current branch is 'fixit'
      And HEAD is 32e1130


  @wip
  Scenario: Error exit when not in Git repository
    Given the working directory is not in a Git repository
     When I issue the command `prev`
     Then the return code is 2
      And stderr output starts with 'Not in a Git repository.'


  @wip
  Scenario: Error exit when working tree is dirty
    Given the working directory is a Git repo
      But the working tree is not clean
     When I issue the command `prev`
     Then the return code is 3
      And stderr output starts with 'Workspace contains uncommitted'


  @wip
  Scenario: Error exit on independent branch
    Given the working directory is a Git repo
      And the current branch is 'master'
     When I issue the command `prev`
     Then the return code is 4
      And stderr output starts with 'Current commit would become unreachable'


  @wip
  Scenario: Error exit on no parent commit
    Given the working directory is a Git repo
      And the current branch is 'root'
     When I issue the command `prev`
     Then the return code is 5
      And stderr output starts with 'No parent commit.'
