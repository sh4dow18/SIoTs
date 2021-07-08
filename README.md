# Sh4dow's IoT Simulator (SIoTs)

![PRESENTATION](files/readme/01_presentation.png)

# Overview

This guide teaches how to install Cisco Packet Tracer, as well as how to use IoT
componentsin a simulated environment where the elements act manually or
automatically so that the user understands how the world of the Internet of
Things works.

I will assume you have basic networking skills and will not explain things like
"IP", netmask or "DHCP".

# What is Cisco Packet Tracer?

Packet Tracer is a powerful network simulation tool designed by Cisco. This helps
you practice creating simple and complex networks on a variety of devices to
improve on all network components not just routers and switches. With this tool,
you can create interconnected solutions for smart cities, homes and businesses.

Packet Tracer functions as a learning environment for Cisco instructional courses,
distance learning, career training, job planning, or just for fun.

![PACKET](files/readme/02_packet_tracer.jpg)

If you want to know more about this, 
**[click here](https://www.netacad.com/courses/packet-tracer)**
 for more information

# Packet Tracer Version

Version: 8.0.0

# Packet Tracer Requirements

	- CPU: Intel Pentium 4, 2,53 GHz or equivalent

	- RAM: 2 GB

	- Storage: 1.4 GB of free disk space

	- Recommended screen resolution: 1024 x 768

# Packet Tracer Installation

To install Cisco Packet Tracer, what you must do is go to the official Cisco website
which is 
**[Netacad](https://www.netacad.com/)**
. Then, you have to create a free Cisco account to get the full functions of the
program, this has to be done in the part that says "Login". Then, having created the
account, you have to enter "Resources" and then "Download Packet Tracer". Next, you
have to download the latest version for 64 bits, that is, the "x64". This works on 
Windows and Linux.

To install it, you must run the installer and follow the steps in it.

# What is IoT?

"IoT" or "Internet of Things" is one of the tools most used today in task automation.
It allows devices to connect and interact with each other, this makes it easy to
perform functions with minimal human participation, such as turning on a light or
activating a camera.

If you want to know more about this topic, you can visit 
**[this site](https://www.zdnet.com/article/what-is-the-internet-of-things-everything-you-need-to-know-about-the-iot-right-now/)**
 for more information

![IOT](files/readme/03_iot.jpg)

# Using SIoTs

![LOGO](files/readme/04_logo.png)

First, you have to download the repository. To download it, you can download the
compressed file (.zip) or clone the repository, with the "git" program installed,
through the CMD in "Windows" or with a terminal in Linux. This is done in the form
(In both cases):

```bash
git clone https://github.com/sh4dow18/SIoTs.git
```

In Linux in some cases the command "sudo" is needed before the previous command

To use the "Shadow's IoT Simulator.pkt" program you have to double click on it, with
Cisco Packet Tracer installed.

This program will display the following:

![SIOTS](files/readme/05_siots.png)

Later, you must wait 1 minute and a half so that all the components are connected
correctly and that the internal programs work in the best way.

Now, there are 3 ways to test how the IoT works in this version:

	- Manually

	- Automatically on the same motherboard

	- Automatically on different motherboards

With the manual option, messages will be sent from a device to control IoT components.
For this, you have to use the cell phone that is connected to the access point.

![SMARTPHONE](files/readme/06_smart_phone.png)

In the smartphone, there is the option "Desktop" (Red Arrow) that has all the applications
that are installed. You have to access to the "MQTT Client" app.

![ADMINDESKTOP](files/readme/07_admin_desktop.png)

Afterwards, the smartphone automatically connects to the server hosted on another network
as the administrator user (Red Square). Then you go to the "Publish" section to enter your
message. The message is divided into 2 parts: The topic and the sub-message (payload). The
topic goes in the first box with a "/" in front of it always and the payload in the second
box (Green Square). Then, you have to press the "Publish" button to send the message to
the server (Blue Arrow).

![ADMINMQTTCLIENT](files/readme/08_admin_mqtt_client.png)

Finally, you can see that by the message all the components connected to the motherboard
turn on or open depending on the component. This happens because of that specific message.

![ALLON](files/readme/09_all_on.png)