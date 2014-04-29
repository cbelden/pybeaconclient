<h2>pybeaconclient</h2>
<h4>Overview</h4>
<p>
The pybeaconclient tool is a Python package that recovers the beacon records from a device running the pybeacon package (a beacon logging tool). Implemented and tested using a MacBook Pro (2010, Mavericks), pybeaconclient is designed to automatically recover all beacon records without affecting the operation of the detecting device.
</p>
<h4>What you need</h4>
<ul>
<li>Rasbperry Pi (tested using a Model B running Raspbian)</li>
<ul>
<li>Must be running <a href="https://github.com/cbelden/pybeacon">pybeacon</a></li>
<li>Additionally, must have a WiFi dongle configured in ad-hoc mode*</li>
</ul>
<li>MacBook Pro (Mavericks)</li>
</ul>
<p>*The Raspberry Pi WiFi dongle needs to be in ad-hoc mode for the client device to connect. This requires the Raspberry Pi's WiFi dongle to have a configured SSID, static IP address, and subnet mask that is known by the client.</p>
<h4>Author Info</h4>
<p>
Calvin Belden<br>
University of Notre Dame<br>
EE Senior Design Project - Team GreenSpace<br>
</p>
