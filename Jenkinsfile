node {
   stage('Get Source Code') {
      git branch: 'main', url: 'https://github.com/ankitkhurana-git/automation-assignment.git'
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
	  if (!fileExists("Jenkinsfile")) {
         error('Dockerfile missing.')
      }
   }
  
}
