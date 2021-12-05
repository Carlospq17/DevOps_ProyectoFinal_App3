node {

    stage('Deploy') {
        //Paramos el contenedor y lo eliminamos
        sh 'docker stop cloud_storage_app || true && docker rm cloud_storage_app || true'
        //Generamos la nueva imagen
        sh 'docker build -t devops_cloud_storage:v${BUILD_NUMBER} .'
        //Creamos el contenedor con la imagen y la iniciamos
        sh 'docker container create --name=cloud_storage_app devops_cloud_storage:v${BUILD_NUMBER}'
        sh 'docker container start cloud_storage_app'
    }
}