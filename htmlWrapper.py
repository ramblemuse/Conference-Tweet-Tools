# -*- coding: utf-8 -*-
# ******************************************************************************
#   These classes provide a Python object wrapper for writing indented HTML5.
#   Objects are created from a tag and an optional list or tuple of attributes.
#
#   Keith Eric Grant (keg@ramblemuse.com
#   02 April 2015
#*******************************************************************************

class element :
    """General class for tagged elements with optional attributes"""

    indent = '  '
    threshold = 81

    def __init__(self, tag, parent=None, attributes=None) :
        self.parent = parent
        self.tag = tag;
        self.contents = []
        if attributes :
            self.contents.append('<{} {}>'.format(tag, ' '.join(attributes)))
        else :
            self.contents.append('<{}>'.format(tag))

    def add_selfclose(self, tag, attributes=None) :
        """Add a self-closing element"""
        if attributes :
            self.contents.append('<{} {} />'.format(tag, ' '.join(attributes)))
        else :
            self.contents.append('<{} />'.format(tag))

    def add_element(self, tag, attributes=None) :
        """Add an element which may contain other elements"""
        self.child = element(tag, self, attributes)
        return self.child

    def add_text(self, text) :
        """Add text within an open element"""
        self.contents.append(text)

    def close(self) :
        """Close an open element, adding its closing tag, doing some
        formatting, and appending its contents onto its parent's contents"""

        self.contents.append("</{}>".format(self.tag))

        # If the elements total line-length will be less than a threshold,
        # just combine everything on one line. Otherwise, indent all of
        # the child elements of this element

        if sum([len(x) for x in self.contents]) < self.threshold :
            self.contents = [''.join(self.contents)]
        else :
            self.contents[1:-1] = [self.indent + x for x in self.contents[1:-1]]

        # Unless this is the root element (i.e. the document itself), move
        # everything for this element into the contents of the parent element.
        if self.parent :
            self.parent.contents.extend(self.contents)
            self.contents = None
            self.parent.child = None


class document (element) :
    """This class inherits from the element class, extending the element class
    only to create the document with an HTML5 DOCTYPE and HTML element and
    adding a method to write out the entire document."""

    def __init__(self) :
        self.parent = None
        self.tag = 'html'
        self.contents = []
        self.contents.append('<html lang="en">')

    def write(self,out) :
        out.write("<!DOCTYPE html>\n")
        out.write("\n".join(self.contents) + "\n")

