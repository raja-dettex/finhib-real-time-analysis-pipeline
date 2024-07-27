terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.11.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}
provider "kubernetes" {
  config_context_cluster = "minikube"
}



resource "kubernetes_namespace" "confluent" {
  metadata {
    name = "confluent"
  }
}

resource "kubectl_manifest" "zookeeper" { 
  yaml_body = file("./manifests/zookeeper-deployment.yaml")
}

resource "kubectl_manifest" "kafka" { 
  yaml_body = file("./manifests/kafka-deployment.yaml")
}

resource "kubectl_manifest" "cassandra" { 
  yaml_body = file("./manifests/cassandra-statefulset.yaml")
}

resource "kubectl_manifest" "spark-master" { 
  yaml_body = file("./manifests/spark-master-deployment.yaml")
}

resource "kubectl_manifest" "spark-worker" { 
  yaml_body = file("./manifests/spark-worker-deployment.yaml")
}

resource "kubectl_manifest" "schema-registry" { 
  yaml_body = file("./manifests/schema-registry-deployment.yaml")
}

resource "kubectl_manifest" "producer" { 
  yaml_body = file("./manifests/producer-deployment.yaml")
}

resource "kubectl_manifest" "kafka-init" { 
  yaml_body = file("./manifests/kafka-init-job.yaml")
}

resource "kubectl_manifest" "schema-init" { 
  yaml_body = file("./manifests/schema-init-job.yaml")
}