# gdemu-sd-tool

## Intro
A tool to help manage SD cards for use with Sega Dreamcasts that have the [GDemu](https://gdemu.wordpress.com/about/) hardware modification. While putting such a disk together isn't difficult by hand, it can be tedious to do so especially if you manage several cards, or want to add / remove / reorder the games on a given disk frequently. This tool helps with that.

There is a Windows app that does this already, but if you run Linux that won't do you much good now will it? This tool probably runs everywhere that Python 3 does, but I only tested it on Linux. I didn't use any exotic libraries though, so really it should work.

## Usage

This is a command line program that accepts a JSON manifest describing how you'd like to organize your games and then makes that happen. It will install the very excellent GDmenu program into the first _slot_ of the card (no need to include it in the JSON manifest) and then puts the games after it, naming everything in the way expected by GDEMU.

It presently expects the games to be in .zip archives, with a single .gdi inside of it as well as the usual .bin and .raw files.

To use it:
1. Insert your SD card
2. Create a single fat partition on it
3. Create a fat32 filesystem on it
4. Mount it some place where you can write
5. Create a JSON manifest as described below
6. Invoke the tool like: `$ ./gst -m /location/of/your/manifest.json -t /mnt/SD`

For steps 1-4 you're on your own; the tool could be made to help with that, but it's really not hard, and I'd rather not take the chance of wiping something important.

## JSON manifest format

The manifest isn't complicated. It should look like:

```
{
    "slots": [
        {
            "name": "The Name of the Game",
            "src": "/the/path/to/this/game.zip"
        },
        {
            "name": "The Name of Another Game",
            "src": "/the/path/to/another/game.zip"
        }
    ]
}
```

The order of the elements in the `slots` array is the order they'll appear in the menu when you boot it up.

## Possible Enhancements

I may never do any of this because what I have now is working for me, but maybe some day...

* Support for more than zipped .gdi formatted games
* Initialize the card for you
* Clean old files automatically
* Check for whether enough free space exists
* Add more error handling

## Acknowledgements

GDEMU - There wouldn't be any point in creating this app without GDEMU existing in the first place. I encourage anyone with a Dreamcast to perform this hardware modification. It's not difficult and will really breath life back into your old hardware.

I didn't write GDmenu, but I consider it essential for effectively using GDEMU. See the readme.txt in the gdmenu directory for attribution. I can't determine if this has a proper site to reliably pull it from, but it doesnt have any license terms attached so I decided to just include a static copy with the tool.

