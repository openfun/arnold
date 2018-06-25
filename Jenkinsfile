podTemplate(label: "arnold", cloud: "openshift", containers: [
    containerTemplate(
        name: "jnlp",
        image: "arnold:1.0.0-alpha",
        alwaysPullImage: true,
        ttyEnable: true,
        workingDir: "/tmp",
        args: '${computer.jnlpmac} ${computer.name}',
        command: "/usr/local/bin/run-jnlp-client"
    )
]) {
    node("arnold") {
        stage("git clone") {
            openshift.withCluster() {
                openshift.withProject() {
                    checkout scm
                    sh "ansible --version"
                }
            }
        }
    }
}
