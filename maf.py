#!/usr/bin/env python
# coding: ISO8859-1
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
maf - a waf extension for automation of parameterized computational experiments
"""

# NOTE: coding ISO8859-1 is necessary for attaching maflib at the end of this
# file.

import os
import os.path
import shutil
import subprocess
import sys
import tarfile
import waflib.Context
import waflib.Logs

TEMPORARY_FILE_NAME = 'maflib.tar.bz2'
NEW_LINE = '#XXX'.encode()
CARRIAGE_RETURN = '#YYY'.encode()
ARCHIVE_BEGIN = '#==>\n'.encode()
ARCHIVE_END = '#<==\n'.encode()

class _Cleaner:
    def __init__(self, directory):
        self._cwd = os.getcwd()
        self._directory = directory

    def __enter__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._cwd)
        if exc_type:
            self.clean()
        return False

    def clean(self):
        try:
            path = os.path.join(self._directory, 'maflib')
            shutil.rmtree(path)
        except OSError:
            pass

def _read_archive(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                raise Exception('archive not found')
            if line == ARCHIVE_BEGIN:
                content = f.readline()
                if not content or f.readline() != ARCHIVE_END:
                    raise Exception('corrupt archive')
                break

    return content[1:-1].replace(NEW_LINE, '\n'.encode()).replace(
        CARRIAGE_RETURN, '\r'.encode())

def unpack_maflib(directory):
    with _Cleaner(directory) as c:
        content = _read_archive(__file__)

        os.makedirs(os.path.join(directory, 'maflib'))
        os.chdir(directory)

        with open(TEMPORARY_FILE_NAME, 'wb') as f:
            f.write(content)

        try:
            t = tarfile.open(TEMPORARY_FILE_NAME)
            t.extractall()
        except tarfile.TarError:
            raise Exception('can not open maflib tar file')
        finally:
            t.close()

        os.remove(TEMPORARY_FILE_NAME)

        maflib_path = os.path.abspath(os.getcwd())
        # sys.path[:0] = [maflib_path]
        return maflib_path

def test_maflib(directory):
    try:
        os.stat(os.path.join(directory, 'maflib'))
        return os.path.abspath(directory)
    except OSError:
        return None

def find_maflib():
    path = waflib.Context.waf_dir
    if not test_maflib(path):
        unpack_maflib(path)
    return path

find_maflib()

def configure(conf):
    try:
        conf.env.MAFLIB_PATH = find_maflib()
        conf.msg('Unpacking maflib', 'yes')
        conf.load('maflib.core')
    except:
        conf.msg('Unpacking maflib', 'no')
        waflib.Logs.error(sys.exc_info()[1])

def options(opt):
    try:
        find_maflib()
        opt.load('maflib.core')
    except:
        opt.msg('Unpacking maflib', 'no')
        waflib.Logs.error(sys.exc_info()[1])
#==>
#BZh91AY&SY�_� Yo����\h������������    `V�����^���4o|�۹���4���D�U;�Z���B#YYY`��^ד��Z5���Ol���v��n�U�����  to�����_{'�}���ڎݷS��=,�)��罴�� �K�[��}����OT��]�9�{�m���{�z<�f�[p��ϞW���(��֊��{�[��݌�St�(>�v��Ϯ�v��>�p�>��ݫ^���[Vͽ�u��|;�Mi�4���ё��A�#YYY  @Ѧ� �� �&��䘩����������z��    hS"	�&=#YYYI�(i�544�� ��4z�!H��i�H�1OiD��򞧓���mG�F�#YYY� �z��"#A0SѢ2i��12i�z�M#A�����#YYY2�hѠTR�#YYY'���i�T�?I�&�􁶨�h� f�g��_�>�x�1�B�H�L�yzF���3��=��$��5�e�z��N��ݮ�TC�@	, � �`L���AT�d?4e~����Ə�#XXX�m��L#��%bZO����R��x�����lK��Z-��B�F��1�THF#��RTX�k�\�2��h9��U��Q �皋ϲւ?��D�0#XXX@�j;�)ȤJF��z�%#aM2%��2##XXX���#�TDWj3�xC����oh6��ՙ�5{8�̜p�����a��C��i���;c�w�vkE4!	@�L7�r��j}����u���rE����@��n�x�2��m�L5�X}B㔻�g���o��ch�#YYY#i�|eRɒַ��kaڞ�a �G��(�>�^�3-���1�y����ݨ|_�eEA�!U��3J$A���)`��л�hçer��H�a�Z��#�M#YYY�WN�?e�rN��V��Ԥ�<�Z�n�Qz,ye����^��_�<x�N���x�jt��nI��d�m��bhq�J��;[�,ء��Tq�*�u����67��S��1a�n����.�HƗ�����[t{&s��%G#XXX�����a��{w���bvY�J*�.���͉YN�:�y:�u[�����d���:۬V�u)R��t:A�چo#XXX�/��G�S�����IVm��*q꾭W�D�wש����0���vv)3�q�	;��ͭv��P�D��,��͏fK�i�a�Ѱ�r=g����������(���ݞ�?^g����zovY ��������AT��8�K��g(��~�V��_�X��;�"��(�r,���\���������y�|�'>��y�=rJ�d��|����ʘ�����������AOS|�������P�#XXX��w���{=?�n@s������w��`�c�RdRC��o?���o����·��%�#��Ϲ.�ћ;)�t�EU.T��Y�(�l��%�S�G3�<1J����m�И�����	F�#���hQ(R���,�%&C��A5�k.MtR�F>{8lf���~\V9��T��N����9��-�$~�Jby�զ�������ð��Wo���;���*4��WLr�/y�^�����CA�O�?��S�G�w��p-Žo�����g��۩�j`��O�\��������8�����Aq��'���W�Q(�<�y�m��Y�ٖ��=&������L��~�X�,��uu�eO�v�-&]��`8��������`#�>�&�q�w�M"�}��7���2<�fF��x��)��ۻ���<��i���v9ۆ<2��yw6�gW�c!���4Ͽ{�#C��`����y�y�WCe����H~��&w�8��56�T�'}`z�nOd�u��x�3#��/;L�������~�X���_S�Q��q#XXX��q��H�(���nuɊ��1/���'%�iW�5��錟���Ǫ!�iúi���U��&�l�;EY���UM���:��r����ŤL�@��	E}UHׂ�l�\}�@�{�7�G�M&3o����!9� jفv `���nr��I�SʂC>vg\��#SLٚSXJP�!y�G˧p�㸠��O��rar���#�O ��,�0�F���� ���yZ�0F�h�-cb�	09V������1jqh�|]A)z�#XXX�7h�J��-��X��wo�7�*bH��A�=|9����^.~p���}j�Aރ��A(:����H���S�v.�S���6m0�9["9|�$t#C���7	[�K��Z��l@�"j�H77�����7�M8�LK� �q��w�Nr��B]�&�����h����4��\�#YYY-(r��� ��	0��M����]�{�1�#YYY�Wa=�9���BiIЮ�K�a���'��.#inst�Y.��H��_�*�j;'�+A�09��DlXC4ֹ�xC��8ZMua�Ԯ0��t��W�7����)��L�.��**�@�GOL��N�>!G,���z�R(��+�N|����ms����\1C&�8�\�HAլ���E�p����6�zJƪGi����GQ�I��C��#YYY���V�o���h�iH��$�����ӹpb�#YYY���KSv��Vx<��2TM��jdg�����Q�΅��29+��7&!(S��7ᒽ-TP*�ء�BE�Q:r��t[8j:�f��1Z���{��%��c�[hR��Ug��(��K��t�JTK㰌JQ��f��(��=�Y�M��#YYY{&X���T�#	)Y7�CAw���7K����OE�ڴ�Bk.�ts�����x���[t�Hw`ӳ���R��Q:w�џ��M�ě�*m%��@v�ӐkEM��HM�c��9�c-���bF�L�2߶��(�T�Am�YH��ڇs���P�	��.�>#XXX���J��թǓ�6 Z����k3� i����5��'+m���x��`v}?�uX�rހ�,l����ߵ�+Jp��C�N�λ¢@�N�^exՒ}|���U�:��=�R�O]C?w&�q睚��<��r��g�n�%����2�b��v:�)O؆��Ħ5�Р�̀=xC�M"r!a��ږ]���OS�&Ny�P�6;\�ۅG�;�K���"�N�+k2��l͚����f�]���Y#XXX��#XXXq�*���%"�"e�h-��gn�tΨ�c�D��[w��	�]�:(�ݷ��U.T@��8;e��?����|h�n[�T����j�7~���v��ܞ�w��� �1�#XXX<kN`;�>5��9�[4���irnt���6����:��#�ؼ�B�ͬ�l�5!�17Sm���f�"ʥ'ee��sJP�]����J�-���	t��2m�I~#��<ь�幔�H�Z��� �g����͢D�2��z�{rm��=���yø6>Hc�@�My�bO����gYc7@B�⠮�uٳmj��8/�h�2\�v'���!������gAn�RK���O&M<�3�i"c]�#���؆XG��銡�x��V\�e5hC����jl7M��#YYY�NC���s�[�@��	�H32��tī��.� � �J�-����$������dbҘ�Z]�,�`�U9]��GE삭a}T�<�L�VL��V`�kX�oF���1A8��-=}�f�#XXXVY�!�y�Aښ	)ct�UGH�x=\�:��}ϙ�։�zYVĄZg�qp�el'I��W~#��w�InR��v:;m�J�B�Da��Í7�����z�;�aӝ��ڎ8q�L�^��o����N��YXtqV�F�]��&�L#XXXh�}A_�iC��=�9�:�X�E�爵��n�]��c�Zۓ%ĻSӨ!4���V�g�G2���߻n�ZP��OafH'4�<�țS9�L�������L�N-Hl�c��p ����%��H��q6����oY�b�%{4c$����b 	c`d���="6'�HA���H:��	�dy���T�g���R9:�����'7Qoǁ';I��t:��o2-�;0||�}�U�I	vvq7��`��f����f2PNO�A巀�l��Y��#XXX��tgE����l��7�8�l�Ã�Vtf7��п||��{������k���q�*+�ѩZ�A���1R�I�K���#�I��N����;�[ܼ����ݜ��}J�6��"��u"c���A��эʂ��{��H���z�H���#XXX���j����'@PP���5��	�����V����?X�~]�>瑂�G��$~���}~�o��_����)�+�Ї�fe�%o�_�����CO�B�BS������ے@�/�C�.|Ӟ����11�!��Y�U��J9ӑEd�U���H�`�<ǿ�R�=I�:w�vBխ�E�_l�U�N�3������N��(���A����UDAjC|z}�\���z�$6��Gn�q������>�q�D��-.��F.�(K������>�3��������gd�h�a��Q���s#YYY�g	3T�O�o�ԒoK��I1���[���WM�\��I�\��:M�����d�ٴ�i-�t���jO���L�C���C�p�<�5Bu�~9�Q��>���x?�{��6�"D��ָ\-f,35b�=�v��|���Er�ഺ$�G����t���Zh#XXX)�C<ck�q�ϊ��wfG2�O<y�ʧ�V{���}{�^s���./X���Jd[�?/U�G���J�m4ޒ���������l���0RJ�}������I�*���8ʄI���ƍ�jLH�ҹ�����!Hxy�kQ��k	:�<��[���8t2C����rvޜv�{OX���?���Bȳ���ME������Jr��l#XXX(H�}��g�F�.�q��.��b��m�Iwc� Ύ��/D��^Hy����ߊW�3x��:�/3�;�X���seQw�#)yV_2�5�H����,*|��͞-zO�%�!7P��7tjq�j3���l5��� ۊ��_���qG����ǻ�����[��������	�I�6~�ǗD�ƿ� P�`8��� }�K&d�#XXX��`�#�T�j�齿'�������L�yxnGp0�7>G�1�7�y����}M�����5�]���}�������S���3��?Q��#p&�@S���n>�tba��+B4�|Dfb>��[��Ao���A�N��}�M��~q�)��t#XXX��ȏ!�!������t�d�0K[<bS��V[�����Q��l��w�~$q��k۬u�	TH���H�nxu�������44)b��ha@���~E�⅂d�-�i��r��g�� �H��0oP���ɳ�=�#:'�}>�f���Uˣ��3/Y�oˉ{.6��A��r�:�����T�b������jCГf��Xڕm��k}��<#XXXŉo/�]K����]�4�d�����oҹK����2@��q��)��#��kج�vwj{t튦L��wR������7��ӆ`� oS�|=V�{s����&��c�|)�﶑���|թ9������ 69��h����T�}��*������:W*����+c݈��F�VF���	4ʆ@}�9<��u0}.9����#XXXlR�_�BÇ�c�����t�������#XXXR���rj#,�L�u���x8M�i=������a�����PN����J�v\�uWU���Vˎ?X�����x�NKnd&��\�A�I�z�!� �#�9��*���fc;0�ּГd��$E ;ŻL�?'��.ٍdMG@��\��l�<�0�e��b÷�E�YT�dKw���_�~�~�ԧ�X���ܭ#YYY�������«� k��,��WZ�����O�mjt[V�V��k͚��<�_�5E��01�k�����/�n�`����[�p��q�mb|)�;�0�ÀL�j=��Y"/-9����`p��S�0�6�p2�m�!�A���Ff��6.����m(�������4@�$���|n���`��ǧ��~���7�O_���d-�,�0��ŷ8P�>Fv��H7$K�5Y�H�[�*%�Dώ�I�Hj�÷=�؇���e]"�$�v}-�n�^҅@�J7�ץO�G�G�Da3e������m@w�~��~��$��)��c��R!.�Q2�C������\b���1�����}�5��#b���c�Iî���`�u���v�Q� i�A�E�w�!�(�~�' ��Q���І	�H&j#XXX��~�;}�7D���I�2\C�G2r��A�1���~(���Ţ"�49u��SVp|Bf��nX�9�i$9�x?)u��Z���G�?�O�f~������0l#YYYJ~�J��27�#YYY9�F?��c�����Ǿ�_��[��RQ��E8ݸ�3�)����&gȤ�ML��a��������rd"��]S�'tZʕ��R�R��pq�M�$s8F^�����OQ�C�h`d~�OY�����ué��g����������������9��#C���'w���3{^-fWJ��!*^��}�����#C/my�P ���D͖#XXXl��2''��#YYY�'+��<�|NE(���w_�+-�'���%�;1�&f��/h������j`�|����OF��'{#q������q>��N!�7$�����O���$�l8`^��}'�y��2s��I\�L�]�i�6�(���N��Цec��C@�ԧ��y]�����02%#YYY<�';E�M}J�Xn����Ӑ�T��s=��31'C������RM��x%9�A��y1�+�^�v�m2?!I�)�=XoW�k���Ƌ�l�<��g����=�s�hhO�y�I�A���&#YYYM�(���ddt���8�p�Hĥ�e�7��0n20=�`d;�f#XXX)�qL�̇F��fK~��p���*�m�=��paJvfO!��Ӵdn�����Q�7�#YYY"s�0jM#YYY�P���ccь>O�}S<�ԷLg�ELP�U>qX��}��?����<S�O�zO�Y���O#�M槼�l�I�MJ���f`�p3������Z�G�������BI/��[e�������������C�*7l$�B����A�!$Am��� ~��4�.z��C��S�������uO}�du��,�?�%T�)P]p\�t�I���?�Mbe��br~q�79����714�}�%��Z����ɦð�+��A�Ε|A�@~�$J�����|���#���R!-1�.s_��⦌�ܦ��2ȟ�ݛLVl���DW ���(�Ä�he%�*1#����n6�Z ������|��Gs�8�x� ��d� �+תp���5�S�=�#XXX:R��N�7GM��4	K�N��!'c��#XXX!��h�c	I�'�v�U[��5��&Zb����n�C��Xl6r��4K���ޱ��#XXX�&ͯOcF�Ɉ9,k���mZN���(��I��O		7\yLa��-�/�7�]�����7䂐%\BH*��̊+�0r&J*I�k�����#XXXK9�NILD�U����-8?�2�lyI�Ý��6L�8$#XXX6VD�hf�f����1��a��Ƿ��3U	����28��r��:O9��C��<Ix�9A�!o��L*>Nj�{7w�\��q�m�f�LꙤ�:8Q,�|Q�}e���7��B��̡���PW�%X(�,�cڡ	%		�1�I�<#�"Դ��O ����	<�>|큷�1F鉗��b3�`ڐ5���ǜ����}��!C�%��o5�̸;��"�{��J����:�|gm�4.�����9�> ��T�;��"J㈟_��#XXX����U5Uhu7?��`�JNU+#XXX������a��� ������ݳ�����G0h�C��H�աwe�_>#YYY�3����iG�`sS�ҝ�;���rb�*UYڐ�fÆ��ҏ�ꙦBHט��!=�k嚉�9�R�� t�I�d��"1��B�)$�x���4@=��G�_��|��_Ә3n�I��L�P}9!؁m�μ��C�-Z�TE�Qa�S�#��u(*�sm���^w��r8V�귛��3A*TP�y�(TM�J���@�)����w=�¹���U�rB�Um�B�	e�I#XXX����*�8Jt<�cgu�\�r���􁵰�U?�-4 D8�;:�1��q�q<�*��1�༓ZL3Lb.�A�$T�X����#XXX�^R�vc�{��p�#YYY4�v/5�8e�< �L��	�.k�;}Ḫ���՞�5�w ?O#BX;4%���LHn�U�{�}T�40�'qQ:�#�93�^��,#YYY0�d) ���/�6�/����8<��l�����u��*���:R%�&s(��ְ3��ԧ(�d�\)�V���Tk&I�|#�3G��3ճʭ��q�&C�#YYY��Aw����Pw�5aǙ�[�S�3Z��kX����K��Q����3�{V���z��$�@DS�3��u�C�QJ��_�~�^ ����.o":�t̀�h*�h����h���5�wI#XXXsM��?�ˏ�P���g��^|�����ˣF�哚�����d��I�9ԇ�LNq��u������������\T�v���"̬_#�i�yv'��D�ã���\������v�@j��a��.0��"���31�1H�Q����%rM�3�bb��FG����4���P1���LW;5��i�J�~=�L�e����˲l�h�I��rZ�q0��V�����0,�ChD$Q�ѕd=�#YYY�0N0��6aI�4;J0�N��:wX������#XXX�$z頖6�g�j���#YYY)�@�A��CDP3���`��h�[D!Ua��J�A'�J��GKΙ4#YYY���6�n�UӬu&�Y��*+:�*�9�;*�8�W��������zKeT}*�`�#XXX�1r���2"̙�"�ڊ`GF�츮;P��tj|��s��+�5nL�v�ˮ�$�^�#YYYC�%�`y�T9`Q�!��M���:ǋ[�w@s�5b�7�0�/M�L�:1>y�Y�%�?����`���{��؆#YYY82B¸��ʳ�=3l�D ���v�nՃ����I�c?O� LU�3�oU��2�H��B��8S�4�����l�n_���I�֢��r)�6�5�.F���B�����uhu@mD��f��C�]ݝ������q�<#]WVGp�]������j�z�����I�?�:���ܩ7OF�;����"��¼�M�w�Ss�bX����	<Ay�t	R��Xx�;�b�н�;�ne��đ��t� �Р��Y�e�Mt�'s�U2ˌ6#XXXAGJ5{�8���X����!��o�u�%��4˙L5 B��bp݂;uɶ�Zna� �b�=�ɍN��li��i�Qv&��7���9�3�4��r���̞xcg�[+�{,sy�r4�GX�N<�n�$�B���������*W4��ѝKW�9�EX�M���	�i&�32����fjH�&��8mĹI��t�p�ޛ�撩�1��;�����LL�s����j�E	�7���kRwհ�Cѝ���{32���+G��>�4(����-�<��(a![ܰ������q�����FW.XFmQ�V�3���:�px-�.��5�#�&�xH��lM��5嵈���,?����9uC"N���?�f~��\�b� Qj"� Ն��S�	�!U�>�t�<�	��$r�d�>\k4�f�+�kp��k�~�����J�'�㳸r�[QRxr��:�M.Є�k��l�ѵ3v�|�C�X[bڻ��w��y岸'���D��q�i�wJ'�4H݌�t�/I���q�(���_>�$�������y7�k#YYYc|�#YYY ���#YYY#YYYK# z#XXXp1	����N�%web�������q�!�S�?<��1M��jl�ݬ��#XXX��X[�^^~O��r�w������W�\w�dD6���#��}AG���0��V�"4���� P��̑�n�x���,�ya�dڛ6�>K �'�#�f�Lܦ�+܎kn���0�������Y�z���)�����e�n�h1�l�#QOd�R\�xޝ���0�C^:'�����p�'�L���1�3PA�2�����0������w����4�sV�ܑ}�+�bG`(�1���)��MM֓�"T2Wi�`�*��d	���η��N�F/fv�g�B�%N�%)[�����fcR��|kg%H�au��f���vu�ٸױy!��� nՈ�G;&V9$�`���T#YYY/	�����~OV���٘A��Ui3ʎ,;BS� !�`�]�!XE���@�W��z� ��&F�%zqKލ�`t���{h�-i^s���j��jA��jC�d�:�|0lS����ߴ ~�i>�<��Oў���@J�Bb~�̘�Yh�KBG���30��Cb�k�j�32ԁ�6ad�e���hq5P�l����7`H��JH�է�ϖT������l���C�Qy2��h#YYY�����	�x}K��=�`j�[#YYY%�q	��i�R8�x�9"h�D3�^�W�3G�S�}��r�稽�x��pS炊\YCU�m���11%۟qa�C�f�G�{G"5���[K��f{I��w,s��M�37{�T����-��<��6{�{����#̔�����/~��Lbw��a��$1�:���mF�B�^�ŶY�=�s, ��1#�&X�!����|���F@{���#XXXӅ�B�vK�8>#YYY8��Hll#YYY��'��e|ﺱMԷ���#,�$"�HԮV��ܦ�,�2S#XXX��D:����6B|#����&#��y�M-3 QB�SH�M%)@�0�9�`_w���At!�2pr+z�����SDAEIETW\�(b�.`�6P�E�d��w���>xej1Rf�S�=�>rHg��NgI�g2�����!5r���mG߶B؇	T#YYY �"����,g[K.�C�����u�6����"eV���_7�kӑ�c��(�o��b�8��X�\ ˺b��R��*��las��#YYYD�@���'�ᅷ!�O�GB~���>�>�8{b�m�ɪʲE��Վ�r8A7S��O�<�����eߤʋ���+ �B5���	)P�^6��Ï�#YYY'M;{_�Y+ͺu4LnW���q����ȼ��B褗�I��λ����;���Q�-�L�	�ϔ�7j���{$�U2�W�q���q�����?�#YYYuJ�RT%Je�xf�p����X���G���|���'C����`��h"XiBBdB�>�\���~�y�8}<��u��K���A��9�5DT��2�J��� ��gU�0��"���t�|x��S4>$���?mE�j�HP�a� n����l<� p��B�j�10�0��rɖ�S�Ꭶ��6��΃�Am�#�$��:ǴH�<�m������Tg����d���<��Z�W݉��.�%�� ��=q�5�#XXX'q�kL��h�k�H����'��j�A˜wB���Z#1�#XXX�T�ZO�v?b}|�:\�h𛄾a1�#YYYY��B��%�ۉ�c�����fN�k�1�޲gpT�����#�q�	���L�	ژ#XXX�c�r?!��v���ޤ�	) �����c�!z9��rt�������~��m�~�ӫ���9�S �I�)�'��]. �Um���x�i �@�Jf�U��͈�o�#YYY�`梍���K@�Dc`��+t�I��pl$Hl��η�)��.㻼�$8��o����{��A���6!���Ws|���2��y��kI$�:�\M"���S� ���a�!���s('�޶�0�c%#]�v*Ux*�YV�6T-�&x-���G+;l��-�({��|�i�hi�`'���Қ.i�m#XXX�t*{<�1҆X���#N��:�X�F\�Qx�#YYY��N=\�ڏ�Ϛ՗)��*������*	"L��4M1w&��V��d��:J�a��$�An��	����D���Q��/����C�e�j�{�$�1pb�����#YYY���s6�Ԇ�v��*7c a�)h#YYY~D9�3lO���[�!H� m�N;�o{�5�E�زq����Ju�K����{���7m#XXX��0/�&;��F��M�9�& ��eLP�T�:.5Aɿ'tɄ#YYY�`�>�8�#��+�I��Xv�u�#XXXe��MT�=s#YYY*J]��8�	!G��*��0��v�H���e��"���Wr\��%K��X�W���qZ���	�Eb��3ӥEԈ���.��)m��n`������Kl�*"��	�Y�=f�Y�&�V��[$�TV�ؚ�B�ǽ�U�1�%�%1 4f)dw��0�J�f\�wG ԏb�69�J�0f#�H��5�;���\���No�q���|�[�2o��Qd�؝�@@�{�XwS�#XXX9r�D0��$X�Q3PI0�7�!��f�6Z��	ѧ�w"h]��aX�CT%S��M0AW0�_6���H��a��=V�|��|:A�K޹`dS���.=��pl�d�1���NN�%�N��9b�lh���W��	&Y3��:�C�-#d�z _x�њ�`x"^Qo��a0�"{���Ɓ�H�x�i���-NxKK�Z�Ce�#XXX��0C0Hd	 �l�CB�ﾲuX��-�����2�8�R�����z`��H{}�c~ą�9~kE�K� �s�%�(�f8�t|��k\�&�> �� ���`(C��41�2�,X�6F�M���~��'1� ��e2�$:��"P%��f�L}�#YYY�=5$F��$�����z������#XXXG���>e�&m�FA�L�D����p�oj���R�(�L�:$5(�IPd�L�SBt� �(J��d���1aTM6G),�-;���+��H|=.�w�P�P�	H) $�mZ]�:�@�P컉{���p�>5���=���:0�w&#XXX2�b�5_�Sr���	&��G :�GͰ14xS�t-!����z `+�� XEaH��zz@{�{��������i<�k�1b�ZH�&ټ��6�C�d����$i�g���,~P��Ge�˒���lu�������n��B�+ ��Ի�@��@���E��fQ4���	�؀�В2^�f��=ٕh\%���ܝeb26�T� Ea\�����ޱ����-3��/�a�՘c�M��P�n]�w=�����K[o�!�����EH�&W����q�*�B�V������6�H��3����ІV<HK���A=����J�&�ia�j-��w�rU�4RS1B�G,�Ħ[�c\/д>�C$L4#�").w�c��#XXXqȮ��(~�؎� EKm��R�s��Đ�4}��6��3����^�¾�[F�^�&��(�FE$K0ADWh��pk0)��5I��7�� .EƊ�UZVL)5X�D��<�*)�r&Ĥ�&L�J�,�2�	��E�kH�j2B`(�"31hP�%���Fc��#XXX�5 Q�S#YYYLBFI��M#��#XXX��Ѭ�H��$#YYY��������jR�*}S�*~!���_�u�[I����;5��v=�,yp1��;�)*��N�*R� 2O	E��Eu�o����BU��3�=ջ##|n��5��uT�:���Џ�l4����x�8Y.�ç.����/���dFBle'�t^b*$�$O{��w�&�1e��B3��#XXX�I#XXX$���#YYY��2#YYYۮ���x�4��H(p[����d�#YYY�S=`�i=���X�?g�Hs����t0`�bz.�0PxRoq��}|s�:�v���CwQ��Dϼa�&�;pr2C#XXX��4�d�T��k׼�;2x���Ux ��MzqBI�y&�#XXXe��G>="�A�t�Qdv,}��[�l�7������3r��j�OLu�b6{����7�y�.[�tvp ��=��+��:�6�7�th!ȜY�Ū�5t�I3&7�K�6	�B*`���@�\!�w$�(�b�����@UU��̨M�hbT�.f]��WSUJ��u���)9�&!�8q/io,��VEj�REA��I� �`���>P:���	5�QE'�����M�w(MI��<L I��T�Y0�o�;����?\KJc(�=�^I��xDa��U�2#�]M�����.<�C��q�vlcI��u.#8-�Ī���3�$B��ӂn����I[3�Aq�E�:�Bd�e�N�A$R�R�j;��;1Ɛ�.���bݝ�A� t�d�;���l>u�Iʒ��ک �<�3����C/-$yp�Ίx����^	;��\x�����C �HM�|,$Ƈ��6�9`�fvd ej��MyH�=P�"�x������0��d�>��;v��geWI�V	x-���錘-2&�e`5����oL'fÎC8���w� ����I�(��ʼu�3E���Y���M�y�� O��f~��th�D$Ԉ���5��������3+5�,�!��(�~H}�W�W��6î^/��y�)*$�]���GޜNp�b&��ZZ<@=���p�h�xA+�-�g�mɜ҂�����*����]�Fg�}��ҋdU�A�`&�2r��Ը2=��baN4r���lv����UR#XXX�-���R�ht�KHM�,h��	#XXX!�+��=)==�r��ݳ6f�N����GpF��Ȇ$�Y�B���R�+���/�tе3l�4�s�N�#�ZN�Y����X1��C^A1SD�������)��X�$�"!J*�*�������z,tɡ�Z�}Ϯ/��>����=��& �>�3����#3k��n-o7V���QH4��"�5ŕ�\2m/Aɡ��;�z.U��3#XXX�����&��LC��d?����q���=s��Yf�;ժJA�9��¦����������w�dPIa4W�K�0��h��D"�c,G�^rʤ�.�� �U��;C��S�ZG<�z*�[��� ��~��I(wI�#XXX�ӱ�ӗӄˊ�U�����.��2M$5	���!(�<FR����<:d�Nc�F�	ʐɩ0�3a�D�c ��u\�:��J󗥚x��͸�c��D�޼�E;1�ts�5�AP�c�&��i������!LU�v��pQǖ|�l;�\�hh�#YYY�Zthta�c�92g[�.�O !�H��(�6m�[ް��s�^��"�NoCӉ���%��԰ȻQ2@]�]�ϕSvS-�~��:�����Y&Ln�S�F��@�"Lj�~m�H���F��W�<�Jt��(]��t�E��C3	�zm��fdAL�fFKEP��-+9Iy��:�w�23�S#YYY����1�Y�$Q��T:HME$)�F�|!P�(��]{04Q��oz&ة3Mx&��e$cb��=�.��aW,���c��L�<y�9:�!.	�~��d�����!b�`��"=��|d�7H���O�tl�1ݧ#���+��b���j껬M@[k��suxC,��YvF��]4g6�QbT!�$��q(g{E�fkZ34M�&fa.3���`�$!U��^��IГ��@}�jO��\�efb�9!"��x�cA]�7��8�pk'�:9�Y��L�%��Hʱ=�}�N��B�Ȱ3��O�����}�f���8����A_q&���,�6{��A$� �&�j1�\?8#YYYX�ww����T��EBEf�R��,�`�5۔���Gș���>��,��Hl\��!4���6��Z��5X��X�j�0}B������������1Ĕ9k��bR���L&A�!���#�@���OK�3��u��FA�4��0|�9�`�ɘ�$/dN��e-2�I������A��9&�T�J��Dv�����0tb:���SNAP3�,��KL/N3��4�f�@b�91�5�Q;W��H�>R�����h�"&�?7Gl��Z��n�dE�~���w�d�^���j�4Jk�&H�#YYY���Ŏ�}���@��J`�hb餤.>�Q�g��"#U�<��jH�7MNA��#YYYkDO��R�1�!.$!�TΠ� QL�'ܘ�⽭�;0�i�`x)��3au}I��ت�GJp�ҫ,�d:HLz˓u�9���S�v�������d�3rbK6#YYY�,X�R]�#YYYȫ::��Pޡ�R1&��C����j�6��	!�В4k�،Q�f�t�Lp1aOX��Ŏ�"h����)�~�Q �A&Uݿ2a���x�hLݙ�6�	M%Z���>f�(X`|F*���j_8�H~2��7�0�&(���a�c�{��C!	�]��}	�~uԲ�QHLڜ����&GCLa�G�C��v�-�����A�&Ul�����8,G�Z�#�X��N}�t$#XXX��2TϘw��$���!�������l[7��_���i�턅������?���}���$��ѱT��w$S�	5���
#<==
