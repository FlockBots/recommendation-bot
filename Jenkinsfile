pipeline {
  agent {
    docker {
      image 'ruby:alpine'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'bundle install'
      }
    }
    stage('Test') {
      steps {
        sh 'bundle exec rspec'
      }
    }
  }
}