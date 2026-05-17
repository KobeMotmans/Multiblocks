![The banner](https://wsrv.nl/?url=https://theblackswitch.com/assets/images/proj/multiblocks/logo_banner.webp&q=100&l=0&ll=true&q=100)

![GitHub License](https://img.shields.io/github/license/KobeMotmans/multiblocks?color=blue)
![GitHub Repo stars](https://img.shields.io/github/stars/KobeMotmans/multiblocks?style=flat&logo=github) ![](https://img.shields.io/badge/install-$pip%20install%20mcmultiblocks-9135a6) ![PyPI - Version](https://img.shields.io/pypi/v/mcmultiblocks) ![Minecraft: from 1.21.2 to latest](https://img.shields.io/badge/Minecraft-Available%20from%201.21.2%20to%20Latest-378736)

## Introduction

Multiblocks is a plugin for the [beet](https://mcbeet.dev/) toolchain. It provides a very user friendly and easy way to create multiblock blueprints with a focus on versatility and performance.

Take a look at [our documentation](https://github.com/KobeMotmans/Multiblocks/wiki)

## Features

### Create multiblock blueprints with ease
You only need a single json file and a structure .nbt file inorder to generate your full fledged multiblock blueprint

![A showcase of how the library is used](https://wsrv.nl?url=https://theblackswitch.com/assets/images/proj/multiblocks/usage_showcase.webp&w=1000&l=0&ll=true&q=100)

### Automatic placement detection
The library marks any blocks that are incorrectly placed. Red for a wrong block, Orange for a wrong blockstate and purple if the block should be air.

![Showcase: placement detection](https://wsrv.nl?url=https://theblackswitch.com/assets/images/proj/multiblocks/placement%20detection.webp&w=300&l=0&ll=true&q=100)

### Outlines
You can easily show an outline for your multiblock so you can visualize the structure without much visual lag.

![](https://wsrv.nl/?url=https://theblackswitch.com/assets/images/proj/multiblocks/outline_showcase.webp&q=100&w=300&l=0&ll=true&q=100)

### Full rotation / mirroring
The library handles full rotation and mirroring of the multiblock. Even the blockstates will change appropriately.

### Extreme versatility
The library offers many different optimized ways to implement and interact with your multiblock structure.
It provides an extensive function set that allows you read any data from your multiblock anytime and configure behaviour however you want.<br><br>
![](https://wsrv.nl?url=https://theblackswitch.com/assets/images/proj/multiblocks/function_list.webp&q=100&w=1000&l=0&ll=true&q=100)

It's also equipped with an event based system through callbacks provided in the json file. This makes it a lot easier to run any functionality once the multiblock is completed.

### Additional conditions

In the json file you can also specify any additional conditions that need to be true inorder for the multiblock to complete. That way you can easily implement custom block detection.
