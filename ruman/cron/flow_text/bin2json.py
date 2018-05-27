# -*- coding:utf-8 -*-

import struct
    
weibo_item_keys = ["sp_type", "uid", "mid", "root_uid", "root_mid", "timestamp", "send_ip", \
"send_port", "net_type", "client_type", "mobile_type", \
"message_type", "audit_status", "client_remark_len", \
"user_fansnum", "user_friendsnum", \
"mid_commentnum", "mid_retweetnum", \
"rootid_commentnum", "rootid_retweetnum", \
"text_length", "pic_url_length", \
"pic_content_length", "audio_url_length", \
"video_url_length", "audio_content_length", \
"video_content_length", "text_length", "text"]

def numToDottedQuad(n):
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n, d)
        q.append(str(m))
        d = d / 256
    return '.'.join(q)

def ip2geo(ip_addr):
    # ip_addr: 236112240
    dottedIpAddr = numToDottedQuad(int(ip_addr))
    return dottedIpAddr

def bin2json(data, total_len, sp_type):
    offset = 190
    uid, mid, root_uid, root_mid, rel_time, send_ip, send_port, net_type, client_type, mobile_type, message_type, audit_status, client_remark_len, user_fansnum, user_friendsnum, mid_commentnum, mid_retweetnum, rootid_commentnum, rootid_retweetnum, text_length, pic_url_length, pic_content_length, audio_url_length, video_url_length, audio_content_length, video_content_length = struct.unpack("!32s32s32s32sIIHBBBBHHIIIIIIHHIHHII", data[:offset])

    sp_type = ord(sp_type)
    send_ip = ip2geo(send_ip)
    
    uid = uid.replace('\x00', '')
    if uid == '':
        return None
    else:
        uid = int(uid)

    mid = mid.replace('\x00', '')
    if mid == '':
        return None

    if ord(root_uid[0]) == 0:
        root_uid = ""
        root_mid = ""
    else:
        root_uid = root_uid.replace('\x00', '')
        if root_uid != '':
            root_uid == int(root_uid)
        root_mid = root_mid.replace('\x00', '')
        
    if client_remark_len != 0:
        fmt = "%ds" % (client_remark_len)
        client_remark = struct.unpack(fmt, data[offset: offset+ client_remark_len])
    else:
        client_remark = ""
    offset += client_remark_len

    if 0 != text_length:
        fmt = "%ds" % (text_length)
	text = struct.unpack(fmt, data[offset: offset + text_length])
	text = text[0].decode('utf8', 'ignore')
    else:
        text = ""
    offset += text_length

    if 0 != pic_url_length:
        fmt = "%ds" % (pic_url_length)
        pic_url = struct.unpack(fmt,data[offset: offset + pic_url_length])
    else:
        pic_url = ""
    offset += pic_url_length

    if 0 != pic_content_length:
        fmt = "%ds" % (pic_content_length)
        pic_content = struct.unpack(fmt, data[offset: offset + pic_content_length])
    else:
        pic_content = ""
    offset += pic_content_length

    if 0 != audio_url_length:
        fmt = "%ds" % (audio_url_length)
        audio_url = struct.unpack(fmt, data[offset: offset + audio_url_length])
    else:
        audio_url = ""
    offset += audio_url_length

    if 0 != audio_content_length:
        fmt = "%ds" % (audio_content_length)
        audio_content = struct.unpack(fmt, data[offset: offset + audio_content_length])
    else:
        audio_content = ""
    offset += audio_content_length

    if 0 != video_url_length:
        fmt = "%ds" % (video_url_length)
        video_url = struct.unpack(fmt, data[offset: offset + video_url_length])
    else:
        video_url = ""
    offset += video_url_length

    if 0 != video_content_length:
        fmt = "%ds" % (video_content_length)
        video_content = struct.unpack(fmt, data[offset: offset + video_content_length])
    else:
        video_content = ""

    if "" == text:
        pass
    else:
        pass
    
    weibo_item_values = [sp_type, uid, mid, root_uid, root_mid, rel_time, send_ip, send_port, net_type, client_type, mobile_type, message_type, audit_status, client_remark_len, user_fansnum, user_friendsnum, mid_commentnum, mid_retweetnum, rootid_commentnum, rootid_retweetnum, text_length, pic_url_length, pic_content_length, audio_url_length, video_url_length, audio_content_length, video_content_length, text_length, text]

    weibo_item = dict()
    for idx, key in enumerate(weibo_item_keys):
        weibo_item[key] = weibo_item_values[idx]

    return weibo_item
