node {
   stage('Get Source Code') {
      git ('https://github.com/ankitkhurana-git/automation-assignment.git')
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
   }
   stage('Build Docker') {
         sh "sudo docker build -t automation-docker ."
   }
   stage("run docker container"){
        sh "sudo docker run -p 5001:5001 --name automation-docker -d automation-docker "
    }
}
