---
date: 2025-02-19
lastmod: 2025-02-20
draft: false
slug: derp
title: Derp
description: Testing out layouts and stuff.
  This is a page bundle (leaf bundle) that groups the content and images in a directory.
---

Veniam esse tenderloin, burgdoggen occaecat laboris turducken salami nulla. Duis sirloin corned beef, consectetur chicken nisi aliquip swine strip steak non aliqua commodo short loin cow frankfurter.

Whether `isFancy` is `true` or `false`, you always have a `<Counter />` as the first child of the `div` returned from the root `App` component.

## This is a test

Bacon ipsum dolor amet doner esse prosciutto incididunt pastrami. Consequat leberkas capicola venison ground round non. Ex est elit alcatra, landjaeger reprehenderit proident. In magna landjaeger esse burgdoggen ut. Eiusmod sint quis chicken labore voluptate nulla fugiat consectetur reprehenderit corned beef venison. Chicken non spare ribs, dolor tail t-bone frankfurter sirloin.

> Ugh! Summer is awful. There's too much pressure to enjoy yourself.

Here's a link to [another post]({{< relref "2025-02-21-derping-with-images" >}}).

{{<img src="17-536x354.jpg"
  alt="Path along the countryside"
>}}

Bresaola ad cupidatat deserunt, corned beef pariatur frankfurter alcatra. Chislic pork loin pig elit esse veniam. Ea meatball doner burgdoggen sirloin cupidatat swine pork belly sint pastrami salami sausage beef ham. Magna doner dolore capicola non cow. Esse pork drumstick aute. Venison doner fatback nostrud. Flank minim beef shank picanha turkey short loin est exercitation strip steak fatback cow ground round meatball proident.

```csharp
[PuzzleInfo(2023, 2, "Cube Conundrum")]
public class Solution : BaseSolution
{
    private static List<SetOfCubes> Tokenize(string line)
    {
        var sets = new List<SetOfCubes>();

        foreach (var elements in line.Split(';', StringSplitOptions.TrimEntries))
        {
            var set = new SetOfCubes();
            var cubes = elements.Split(',', StringSplitOptions.TrimEntries);

            foreach (var cube in cubes)
            {
                (int number, string color) = cube.Split() switch { var x => (Convert.ToInt32(x[0]), x[1]) };
                set[color] = number;
            }

            sets.Add(set);
        }

        return sets;
    }
}
```

Sirloin culpa et, aliqua pork pancetta beef consequat strip steak ut ullamco esse sed.

- Sint veniam beef
- Ball tip in ribeye short ribs venison pork ut

Anim beef ea jerky sed culpa pariatur ham hock adipisicing eu fatback duis.

1. Strip steak irure nulla bacon tempor meatball est deserunt
1. Short loin eu commodo lorem ball tip boudin pork belly
1. Beef sed chislic velit sirloin pariatur sausage ut aliquip occaecat

This is a paragraph.
