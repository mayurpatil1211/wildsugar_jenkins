def img
pipeline {
    environment {
        registry = "mayurpatil1211/wildsugar_jenkins" //To push an image to Docker Hub, you must first name your local image using your Docker Hub username and the repository name that you created through Docker Hub on the web.
        registryCredential = 'dockerhub'
        githubCredential = 'github'
        dockerImage = ''
    }
    agent any
    stages {
        
        stage('checkout') {
                steps {
                git branch: 'main',
                credentialsId: githubCredential,
                url: 'https://github.com/mayurpatil1211/wildsugar_jenkins.git'
                }
        }
        
        stage ('Test'){
                steps {
                  
                    
                    echo '********************Running tests*********'
                    sh "printenv"
                    sh "ls -l"
                    sh "cd wild_sugar"
                    sh 'pip3 install -r requirements.txt'
                    sh "python3 -m pytest -v"
                    // 
                }
            }
        
        
        // stage ('Clean Up'){
        //     steps{
        //         sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
        //         sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
        //         sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
        //     }
        // }

        // stage('Build Image') {
        //     steps {
        //         script {
        //             img = registry + ":${env.BUILD_ID}"
        //             println ("${img}")
        //             dockerImage = docker.build("${img}")
        //         }
        //     }
        // }

        // stage('Push To DockerHub') {
        //     steps {
        //         script {
        //             docker.withRegistry( 'https://registry.hub.docker.com ', registryCredential ) {
        //                 dockerImage.push()
        //             }
        //         }
        //     }
        // }
                    
        // stage('Deploy') {
        //   steps {
        //         sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
        //   }
        // }

      }
    }