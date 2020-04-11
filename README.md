# gdemu-sd-tool

## Intro
A tool to help manage SD cards for use with Sega Dreamcasts that have the [GDemu](https://gdemu.wordpress.com/about/) hardware modification. While putting such a disk together isn't difficult by hand, it can be tedious to do so especially if you manage several cards, or want to add / remove / reorder the games on a given disk frequently. This tool helps with that.

There is a Windows app that does this already, but if you run Linux that won't do you much good now will it? This tool probably runs everywhere that Python 3 does, but I only tested it on Linux. I didn't use any exotic libraries though, so really it should work anywhere.

## Usage

This is a command line program that accepts a JSON manifest describing how you'd like to organize your games and then makes that happen. It will install the very excellent GDmenu program into the first _slot_ of the card (no need to include it in the JSON manifest) and then puts the games after it, naming everything in the way expected by GDEMU.

It presently expects the games to either be in .zip archives or extracted to directories, with a single .gdi as well as the usual .bin and .raw files. I don't have any .cdi images other than GDmenu so I don't know how those work, but naive support for those is included too in that the tool will rename a .cdi file to 'disc.cdi' and put any other files in the directory along side it unchanged. If this isn't good enough, I'm interested in adding the proper support, so reach out.

Most .gdi files already contain references to .bin and .raw files that are named in a compatible manner for GDEMU, but some don't - and the tool is smart enough to rewrite the .gdi files to refer to files that GDEMU can handle, and then to rename those files to match. If there are examples that don't work, I'd like to know about that too.

To use it:
1. Insert your SD card
2. Create a single fat partition on it
3. Create a fat32 filesystem on it
4. Mount it some place where you can write
5. Create a JSON manifest as described below
6. Invoke the tool like: `$ ./gst -m /location/of/your/manifest.json -t /mnt/SD`

For steps 1-4 you're on your own; the tool could be made to help with that, but it's really not hard, and I'd rather not take the chance of wiping something important.

The tool will place a file named `name.txt` into each game folder which contains the name of the game. It will also copy the manifest to the root of the SD card named `manifest.json`.

I haven't added any logic to make the tool smart enough to recognize when a folder already contains the right game, so instead (at least for now) you'll need to purge what's there before you run the tool, and it has to do all the work every time it runs. Sorry.

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
        },
        {
            "name": "The Name of Yet Another Game",
            "src": "/the/path/to/yet/another/game/directory"
        }
    ]
}
```

The order of the elements in the `slots` array is the order they'll appear in the menu when you boot it up (after GDmenu).

## Possible Enhancements

I may never do any of this because what I have now is working for me, but maybe some day...

* Support for more archive types (it should be reasonably easy)
* (Optionally) Initialize the card for you
* Clean old files automatically
* Check whether a slot already contains the correct game
* Check for whether enough free space exists
* Add more error handling
* Clean up the verbose output and what is emitted to stdout/stderr

## Acknowledgements

GDEMU - There wouldn't be any point in creating this app without GDEMU existing in the first place. I encourage anyone with a Dreamcast to perform this hardware modification. It's not difficult and will really breath life back into your old hardware.

I didn't write GDmenu, but I consider it essential for effectively using GDEMU. See the readme.txt in the gdmenu directory for attribution. I can't determine if this has a proper site to reliably pull it from, but it doesnt have any license terms attached so I decided to just include a static copy with the tool.
