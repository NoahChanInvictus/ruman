�ļ�˵����
global_utils.py  �����ļ�
test_code.py �����ļ������������ã�
protou.py ���������û������˿�б��γ������û�Ⱥ��ѵ����ʱ����Ҫ��
find_users.py ����uid��ѯ�û��ı�����Ϣ�ͷ�˿�ṹ
domain_by_text.py �����û�΢���ı�������ݷ���
test_domain_v2.py �û��������������

ʹ��˵����
from test_domain_v2 import domain_classfiy

domain_classfiy�����������˵����
�����롿 
uid_list:uid�б� [uid1,uid2,uid3,...]
uid_weibo:�ִ�֮��Ĵ�Ƶ�ֵ�  {uid1:{'key1':f1,'key2':f2...}...}

������� domain����ǩ�ֵ䣬re_label���Ƽ���ǩ�ֵ�
ʾ����
domainʾ����
{uid1:[label1,label2,label3],uid2:[label1,label2,label3]...}
ע��label1�Ǹ��ݷ�˿�ṹ����Ľ����label2�Ǹ�����֤���ͷ���Ľ����label3�Ǹ����û��ı�����Ľ��

re_labelʾ����
{uid1:label,uid2:label2...}
