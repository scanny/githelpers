Feature: Move current branch "upward" to "next" (child) commit
  In order to incrementally traverse a commit history
  As a developer using Git
  I need a way to move the current branch upward, one commit at a time


  Scenario: Move current branch up one commit
    Given the working directory is a Git repo
      And the current branch is 'fixit'
     When I issue the command `next`
     Then the current branch is 'fixit'
      And HEAD is 36c9fec


  Scenario: Error exit when not in Git repository
    Given the working directory is not in a Git repository
     When I issue the command `next`
     Then the return code is 2
      And stderr output starts with 'Not in a Git repository.'


  Scenario: Error exit when working tree is dirty
    Given the working directory is a Git repo
      And the current branch is 'fixit'
      But the working tree is not clean
     When I issue the command `next`
     Then the return code is 3
      And stderr output starts with 'Workspace contains uncommitted'


  Scenario: Error exit on no child
    Given the working directory is a Git repo
      And the current branch is 'spike'
     When I issue the command `next`
     Then the return code is 4
      And stderr output starts with 'No next commit.'


  Scenario: Error exit on more than one child
    Given the working directory is a Git repo
      And the current branch is 'fixit'
      And the current commit is bb695ff
     When I issue the command `next`
     Then the return code is 5
      And stderr output starts with 'More than one child.'
