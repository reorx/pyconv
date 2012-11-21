
Reopen the file with specialfied encoding::

    :e ++enc={encoding}

Run vim command after open vim::

    $ vim -c "execute \"BundleInstall\" | q | q"

Change (convert)::

    :set fileencoding={encoding}

Show encoding::

    :set fileencoding

Convert in commandline::

    $ vim +"set fileencoding=utf-8 | wq"

or::

    $ vim -c "e ++enc=utf8 | set fileencoding=gbk | w\! | q\!" gbk.txt
