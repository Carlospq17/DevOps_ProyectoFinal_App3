node {

    stage('Deploy') {
        //Paramos el contenedor y lo eliminamos
        sh 'docker stop cloudStorageApp || true && docker rm cloudStorageApp || true'
        //Generamos la nueva imagen
        sh 'docker build -t devopsCloudStorage:v${BUILD_NUMBER} .'
        //Creamos el contenedor con la imagen y la iniciamos
        sh 'docker container create --name=cloudStorageApp devopsCloudStorage:v${BUILD_NUMBER}'
        sh 'docker container start cloudStorageApp'
    }
}