---
title: Using various ipywidgets libraries within a Solara application
description: Solara can work with virtually any ipywidget library, and enables powerful interactivity with libraries like ipyleaflet, ipydatagrid, and bqplot.
---
# How can I use ipywidget library X?

Solara can work with any ipywidget library, such as [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet), [ipydatagrid](https://github.com/bloomberg/ipydatagrid) or [bqplot](https://github.com/bqplot/bqplot).

After `solara` is imported, every widget class has an extra `.element(...)` method added to itself. This allows us to create elements for all existing widgets. For example using regular ipywidgets:

```python
import ipywidgets
button_element = ipywidgets.Button.element(description="Click me")
```

## Example with ipyleaflet

For instance, if we want to use ipyleaflet using the classical ipywidget API, we can do:

```python
import ipyleaflet

map = ipyleaflet.Map(center=(52, 10), zoom=8)

marker = Marker(location=(52.1, 10.1), draggable=True)
m.add_layer(marker)
```

In Solara, we should not create widgets, but elements instead. We can create elements using the `.element(...)` method. This method takes the same arguments as the widget constructor, but returns an element instead of a widget. The element can be used in the same way as a widget, but it is not a widget. It is a special object that can be used in Solara.

However, how do we add the marker to the map? The map element object does not have an `add_layer` method. That is the downside of using the React-like API of Solara. We cannot call methods on the widget
anymore. Instead, we need to pass the marker to the layers argument. That, however, introduces a new problem. Ipyleaflet by default adds a layer to the map when it is created, and the `add_layer` adds the second layer. We now need to manually add the map layer ourselves.

Putting this together.
```solara
import ipyleaflet
import solara

url = ipyleaflet.basemaps.OpenStreetMap.Mapnik["url"]

@solara.component
def Page():
    marker = ipyleaflet.Marker.element(location=(52.1, 10.1), draggable=True)
    map = ipyleaflet.Map.element(
        center=(52, 10),
        zoom=8,
        layers=[
            ipyleaflet.TileLayer.element(url=url),
            marker,
        ],
    )
```

Note that this is about the worst example of something that looks easy in ipyleaflet using the classical API becoming a bit more involved in Solara.
In practice, this does not happen often, and your code in general will be shorter and more readable.

Another thing of note is that ipyleaflet uses CSS `z-index` to layer content, potentially causing issues with your map overlaying other content. This can be avoided by styling the parent element of the map with `isolation: isolate;`. For examples of how to do this, you can see the below examples.

See also [the basic ipyleaflet example](/examples/libraries/ipyleaflet) and [the advanced ipyleaflet example](/examples/libraries/ipyleaflet_advanced).

## Example with ipywidgets

Most widgets in (classic) ipywidgets can be used without problems in Solara. Two widgets stand out that are difficult to use.

### Image

The `Image` widget can be used normally, but we cannot use the factory methods like `Image.from_file` and `Image.from_url`, for this reason we create the [Image](/api/image) component that
makes this easier.

### Video

The `Video` widget does not have a corresponding component in solara (yet), but we can manually fill in the `value`. For example:

```solara
import solara
import ipywidgets

url = 'https://user-images.githubusercontent.com/1765949/240697327-25b296bd-72c6-4412-948b-2d37e8196260.mp4'


@solara.component
def Page():
    ipywidgets.Video.element(value=url.encode('utf8'),
        format='url',
        width=500
    )

```

## Wrapper libraries

However, because we care about type safety, we generate wrapper components for some libraries. This enables type completion in VSCode, type checks with VSCode, and mypy.

The following libraries are fully wrapped:

  * `ipywidgets` wrapper: `reacton.ipywidgets`
  * `ipyvuetify` wrapper: `reacton.ipyvuetify`
  * `bqplot` wrapper: `reacton.bqplot`
  * `ipycanvas` wrapper: `reacton.ipycanvas`

This allows us to do instead:
```python
import reacton.ipywidgets as w
button_element = w.Button(description="Click me)
```

And enjoy auto complete and type checking.

## Create your own wrapper

The best example would be to take a look at the source code for now:

  * [ipywidgets](https://github.com/widgetti/reacton/blob/master/reacton/ipywidgets.py)
  * [bqplot](https://github.com/widgetti/reacton/blob/master/reacton/bqplot.py)
  * [ipyvuetify](https://github.com/widgetti/reacton/blob/master/reacton/ipyvuetify.py)

The code is generated by executing:

    $ python -m reacton.ipywidgets


## Limitation

Reacton assumes the widget constructor arguments match the traits. If this is not the case, this may result in runtime errors. If this leads to issues, please open an [Issue](https://github.com/widgetti/solara/issues/new) to discuss this.
