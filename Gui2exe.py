# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Copyright (C) 2009 Free Software Fundation

# auteur : pzia <paparazzia@gmail.com>

# Ce script ne sert qu'a confectionner une distribution binaire pour Win32

# Notes - Etapes pour utiliser ce script :
# 0. Il vous faut :
# - un os Win32
# - une distribution de python 2.6 pour Win32 : http://www.python.org/download/
# - py2exe pour python 2.6
#1. Installation python et ses libs
# - installer les exe python avec les choix par défaut
# - ouvrir une console (Démarrer Executer cmd [Ok]
# - ajouter python dans le path SET PATH=%PATH%;c:\Python23
# - se placer dans le répertoire de iCalendar...
# - python setup.py build
# - python setup.py install
# - Nlconverter doit maintenant être fonctionnel par simple double clic sur le fichier
# 2. Compiler
# - "python Gui2exe.py"
# => le sous-répertoire 'dist' contient la distribution binaire
# - That's it !

from distutils.core import setup
import sys

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")

# nécessaire pour aider py2exe a résoudre les dépendances de SOAPpy et de ClientCooki
import NlconverterLib
import email.Iterators
import email

# lib de transformation en binaire.
import py2exe

# Contiendra la listes des fichiers .py a copier
listModulesFiles = []

version = "0.1.0"

# Setup de distutils
setup(
    console=["Gui.py"], # fichier racine
    data_files=[ # listes des fichiers addtionnels
        ("",["NlconverterLib.py"]),
        ],
    name='Nlconverter',
    version=version,
    description='Nlconverter - Convert Nsf files to something else...',
    options={
        "py2exe" : {
#            "includes" : ['email.Charset', 'email.Encoders', 'email.Errors', 'email.Generator', 'email.Header', 'email.Iterators', 'email.MIMEAudio', 'email.MIMEBase', 'email.MIMEImage', 'email.MIMEMessage', 'email.MIMEMultipart', 'email.MIMEText', 'email.Message', 'email.Parser', 'email.Utils', 'email.base64MIME', 'email.quopriMIME'],
            #"excludes" : ['M2Crypto', 'psyco', 'psyco.classes', 'pyGlobus',
#                          'pyGlobus.io', 'win32evtlog', 'win32evtlogutil',
#                          'xml.dom.ext', 'xml.ns', 'String'],
            "optimize": 2,
            "packages" : ["encodings","email"]}},
    author='paparazzia@gmail.com',
    url='https://github.com/pzia/nlconverter',
    )
