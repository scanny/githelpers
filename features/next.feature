Feature: Move current branch "upward" to "next" (child) commit
  In order to incrementally traverse a commit history
  As a developer using Git
  I need a way to move the current branch upward, one commit at a time


  @wip
  Scenario: Move current branch up one commit
    Given the working directory is a Git repo
      And the current branch is 'fixit'
     When I issue the command `next`
     Then the current branch is 'fixit'
      And HEAD is 36c9fec


  @wip
  Scenario: Error exit when not in Git repository
    Given the working directory is not in a Git repository
     When I issue the command `next`
     Then the return code is 2
      And stderr output starts with 'Not in a Git repository.'


  @wip
  Scenario: Error exit when working tree is dirty
    Given the working directory is a Git repo
      And the current branch is 'fixit'
      But the working tree is not clean
     When I issue the command `next`
     Then the return code is 3
      And stderr output starts with 'Workspace contains uncommitted'


  @wip
  Scenario: Error exit on no child
    Given the working directory is a Git repo
      And the current branch is 'spike'
     When I issue the command `next`
     Then the return code is 4
      And stderr output starts with 'No next commit.'


  @wip
  Scenario: Error exit on more than one child
    Given the working directory is a Git repo
      And the current branch is 'fixit'
      And the current commit is 99ec480
     When I issue the command `next`
     Then the return code is 5
      And stderr output starts with 'More than one child.'
