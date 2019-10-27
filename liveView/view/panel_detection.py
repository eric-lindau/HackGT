#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: panel_detection.py
Description: Detection Panel for Python SDK sample.
"""

import wx

import util
import model
from view import base


import threading
import time
from azure.storage.blob import BlockBlobService, PublicAccess


class DetectionPanel(base.MyPanel):
    """Detection Panel."""

    def __init__(self, parent):
        super(DetectionPanel, self).__init__(parent)

        util.CF.BaseUrl.set("https://emotiontrack.cognitiveservices.azure.com/face/v1.0")
        util.CF.Key.set("4a1e0d41a8494d71ac0b9028464d8e62")

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.hsizer = wx.BoxSizer()
        self.hsizer.AddStretchSpacer()

        self.hvsizer = wx.BoxSizer(wx.VERTICAL)
        self.hvsizer.SetMinSize((util.INNER_PANEL_WIDTH, -1))

        # label = ("To detect faces in an image, click the 'Choose Image' "
        #          "button. You will see a rectangle surrounding every face "
        #          "that the Face API detects. You will also see a list of "
        #          "attributes related to the faces.")
        # self.static_text = wx.StaticText(self, label=label)
        # self.static_text.Wrap(util.INNER_PANEL_WIDTH)
        # self.hvsizer.Add(self.static_text, 0, wx.ALL, 5)

        self.vhsizer = wx.BoxSizer()
        self.vhsizer.SetMinSize((util.INNER_PANEL_WIDTH, -1))

        self.lsizer = wx.BoxSizer(wx.VERTICAL)
        self.lsizer.SetMinSize((util.MAX_IMAGE_SIZE, -1))

        # flag = wx.EXPAND | wx.ALIGN_CENTER | wx.ALL
        # self.btn = wx.Button(self, label='Choose Image')
        # self.lsizer.Add(self.btn, 0, flag, 5)
        # self.Bind(wx.EVT_BUTTON, self.OnChooseImage, self.btn)

        flag = wx.ALIGN_CENTER | wx.ALL
        self.bitmap = base.MyStaticBitmap(self)
        self.lsizer.Add(self.bitmap, 0, flag, 5)

        self.vhsizer.Add(self.lsizer, 0, wx.ALIGN_LEFT)
        self.vhsizer.AddStretchSpacer()

        self.rsizer = wx.BoxSizer(wx.VERTICAL)
        self.rsizer.SetMinSize((util.MAX_IMAGE_SIZE, -1))

        style = wx.ALIGN_CENTER
        flag = wx.ALIGN_CENTER | wx.EXPAND | wx.ALL
        self.result = wx.StaticText(self, style=style)
        self.rsizer.Add(self.result, 0, flag, 5)

        flag = wx.ALIGN_LEFT | wx.EXPAND | wx.ALL
        self.face_list = base.MyFaceList(self)
        self.rsizer.Add(self.face_list, 1, flag, 5)

        self.vhsizer.Add(self.rsizer, 0, wx.EXPAND)

        self.hvsizer.Add(self.vhsizer)

        self.hsizer.Add(self.hvsizer, 0)
        self.hsizer.AddStretchSpacer()

        self.vsizer.Add(self.hsizer, 3, wx.EXPAND)

        self.log = base.MyLog(self)
        self.vsizer.Add(self.log, 1, wx.EXPAND)

        self.SetSizerAndFit(self.vsizer)

        t = threading.Thread(target=self.loop, args=())
        t.start()

    @util.async
    def detect(self, path):
        """Async detection."""
        self.log.log('Request: Detecting {}'.format(path))
        self.face_list.Clear()
        self.face_list.Refresh()
        self.rsizer.Layout()
        self.vhsizer.Layout()

        try:
            attributes = (
                'age,gender,headPose,smile,facialHair,glasses,emotion,hair,'
                'makeup,occlusion,accessories,blur,exposure,noise')
            res = util.CF.face.detect(path, False, False, attributes)
            faces = [model.Face(face, path) for face in res]
            self.face_list.SetItems(faces)
            util.draw_bitmap_rectangle(self.bitmap, faces)

            log_text = 'Response: Success. Detected {} face(s) in {}'.format(
                len(res), path)
            self.log.log(log_text)
            text = '{} face(s) has been detected.'.format(len(res))
            self.result.SetLabelText(text)
        except util.CF.CognitiveFaceException as exp:
            self.log.log('Response: {}. {}'.format(exp.code, exp.msg))

        self.rsizer.Layout()
        self.vhsizer.Layout()

    def get_latest_blob(self, path):
        blob_name = "hackgt19"
        blob_key = "24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ=="
        container_name = 'imageblobs'
        try:
            # Create the BlockBlockService that is used to call the Blob service for the storage account
            block_blob_service = BlockBlobService(account_name=blob_name, account_key=blob_key)

            blobs_list = block_blob_service.list_blobs(container_name)
            # latest_blob = None
            latest_ts = 0
            for blob in blobs_list:
                ts = int(blob.name)
                if ts > latest_ts:
                    latest_ts = ts
                    latest_blob = blob
            
            block_blob_service.get_blob_to_path(container_name, str(latest_ts), path)
            print("Downloaded latest blob Successful")

        except Exception as e:
            print("Error: {}".format(e))

    def loop(self):
        save_path = "./blob.jpg"
        while(True):
            self.get_latest_blob(save_path)
            self.bitmap.set_path(save_path)
            self.detect(save_path)
            time.sleep(2.0)
