jenkins-ci
==========

![](http://jenkins-ci.org/sites/default/files/jenkins_logo.png)

Installs and configures Jenkins CI Server

Version v0.4.0

[![Install](https://raw.github.com/qubell-bazaar/component-skeleton/master/img/install.png)](https://express.qubell.com/applications/upload?metadataUrl=https://raw.github.com/qubell-bazaar/component-jenkins/v0.4.0/meta.yml)

Features
--------

 - Install and configure Jenkins CI Server on multiple compute
 - Setup Jenkins slave nodes
 - Install Jenkins plugins
 - Restore from previosly created backups

Configurations
--------------
 - Jenkins CI 1.xxx (latest), CentOS 6.4 (us-east-1/ami-ee698586), AWS EC2 m1.small, root
 - Jenkins CI 1.xxx (latest), amazon-linux (us-east-1/ami-1ba18d72), AWS EC2 m1.small, ec2-user
 - Jenkins CI 1.xxx (latest), Ubuntu 12.04 (us-east-1/ami-d0f89fb9), AWS EC2 m1.small, ubuntu


Pre-requisites
--------------
 - Configured Cloud Account a in chosen environment
 - Either installed Chef on target compute OR launch under root
 - Internet access from target compute:
   - Jenkins distribution
   - S3 bucket with Chef recipes: qubell-starter-kit-artifacts
   - If Chef is not installed: please install Chef 10.16.2 using http://www.opscode.com/chef/install.sh ```bash <($WGET -O - http://www.opscode.com/chef/install.sh) -v $CHEF_VERSION```

Implementation notes
--------------------
 - Installation is based on Chef recipes from https://github.com/opscode-cookbooks/jenkins/

Configuration parameters
------------------------
 - input.server-os: You can select one of OS listed to run jenkins server
 - agent-type: Allow select slave agent type. For Linux slave nodes you can choose either "jnlp" or "ssh" type. Windows nodes support only "jnlp" agent type. Field type is "string"
 - input.slave-windows-os: Allow set Windows server AMI and it's credentials. Field type is "object"
 - input.slave-windows-instance-size: Here you can choose one of the AWS images types to run Windows OS server. Filed type is "string"
 - input.plugins-info: This field let specify list of plugins to install. Field type is "array"
 - input.slave-windows-user-password: Here you can specify which password should be set to Administrator user in Windows OS

Example usage
-------------
```
- install-jenkins-server:
    action: chefsolo
    precedingPhases: [provision-server-vm]
    parameters:
      recipeUrl: "{$.recipe-url}"
      runList: [ "recipe[cookbook_qubell_jenkins::default]" ]
      roles: [ server ]
      jattrs:
        qubell_jenkins: 
          version: "{$.jenkins-version}"
          plugins: "{$.plugins-info}"
          backup_uri: "{$.backup-uri}"
          restore_type: "{$.restore-type}"
        jenkins:
          server:
            host: "{$.jenkins-server-hosts[0]}"
            port: "{$.jenkins-server-port}"
            install_method: "{$.install-method}"
    output:
      server-attrs: chefState

- install-jenkins-slave:
    action: chefsolo
    precedingPhases: [provision-slave-linux-vm, install-jenkins-server]
    parameters:
      recipeUrl: "{$.recipe-url}"
      runList: [ "recipe[cookbook_qubell_jenkins::node]" ]
      roles: [ slave-linux ]
      jattrs:
        jenkins:
          server:
            url: "http://{$.jenkins-server-hosts[0]}:{$.jenkins-server-port}"
            pubkey: "{$.server-attrs['*'].jenkins.server.pubkey[0]}"
          node:
            agent_type: "{$.slave-linux-agent-type}"
            availability: "{$.slave-linux-availability}"
          cli:
            username: "admin"
            password: "{$.server-attrs['*'].jenkins.server.admin_password[0]}"
    output:
      slave-attrs: chefState
``` 
