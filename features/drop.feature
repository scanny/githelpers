Feature: Drop a commit from revision history
  In order to get rid of an unwanted mid-branch commit
  As a developer using Git
  I need a way to drop a single commit


  @wip
  Scenario: Drop a mid-branch commit
    Given the working directory is a Git repo
      And the current branch is 'fixit'
      And rev c4b6209 is reachable
     When I issue the command `drop c4b6209`
     Then rev c4b6209 is not reachable
      And the current branch is 'fixit'


  @wip
  Scenario: Error exit when not in Git repository
    Given the working directory is not in a Git repository
     When I issue the command `drop c4b6209`
     Then the return code is 2
      And stderr output starts with 'Not in a Git repository.'


  @wip
  Scenario: Error exit when working tree is dirty
    Given the working directory is a Git repo
      But the working tree is not clean
     When I issue the command `drop c4b6209`
     Then the return code is 3
      And stderr output starts with 'Workspace contains uncommitted'


  Scenario: Error exit on commit not reachable
    Given the working directory is a Git repo
     When I issue the command `drop f00beef`
     Then the return code is 4
      And stderr output starts with 'Unknown revision f00beef.'


  Scenario: Error exit on commit reachable from more than one ref
    Given the working directory is a Git repo
     When I issue the command `drop 36c9fec`
     Then the return code is 5
      And stderr output starts with 'Commit 36c9fec reachable from more than'


  @linear-repo
  Scenario: Error exit on commit has no parent
    Given the working directory is a Git repo
     When I issue the command `drop 1985579`
     Then the return code is 6
      And stderr output starts with 'Commit 1985579 has no parent.'


  Scenario: Error exit on commit has more than one parent
    Given the working directory is a Git repo
     When I issue the command `drop f67ea7e`
     Then the return code is 7
      And stderr output starts with 'Commit f67ea7e has more than one parent'
