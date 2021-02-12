# Networking Stress Tester

This application allows Linux users to test the resilience of networking protocols to ensure reliability when real-world networking errors occur. By using the `tc` command's `netem` functionality, rules can be applied to a networking interface. The scripts provided in this repository make it more user-friendly to use.

The following functionalities are supported:
* Packet delaying
    * Supports random delays
        * Note: This causes packets to arrive un-ordered
    * Uniform and gaussian distributions
* Packet dropping
    * Randomly drop a specified percentage of packets
* Packet duplication
    * Randomly duplicate a specified percentage of packets
* Packet corrupting
    * Flip a random bit in a specified percentage of packets
