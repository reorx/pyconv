Japanese Encodings Problem
==========================

One problem I had encountered in development is the strange behavior of shift_jis encoding.

After searching for more information, I found it an historical problem between Unicode and several Japanese encodings.

So I extract some of the documents here, as a study note, and a proof that encoding in programming always sucks.


Wikipedia
---------

http://en.wikipedia.org/wiki/Unicode#Mapping_to_legacy_character_sets

**Mapping to legacy character sets**

Injective mappings must be provided between characters in existing legacy character sets and characters in Unicode to facilitate conversion to Unicode and allow interoperability with legacy software. Lack of consistency in various mappings between earlier Japanese encodings such as Shift-JIS or EUC-JP and Unicode led to round-trip format conversion mismatches, particularly the mapping of the character JIS X 0208 '～' (1-33, WAVE DASH), heavily used in legacy database data, to either U+FF5E ～ fullwidth tilde (in Microsoft Windows) or U+301C 〜 wave dash (other vendors).

Some Japanese computer programmers objected to Unicode because it requires them to separate the use of U+005C \ reverse solidus (backslash) and U+00A5 ¥ yen sign, which was mapped to 0x5C in JIS X 0201, and a lot of legacy code exists with this usage. (This encoding also replaces tilde '~' 0x7E with overline '¯', now 0xAF.) The separation of these characters exists in ISO 8859-1, from long before Unicode.


Debian Doc
----------

http://www.debian.org/doc/manuals/intro-i18n/ch-codes.en.html#s-646problem

**4.4.3.5 ISO 646-* Problem**

You will need a codeset converter between your local encodings (for example, ISO 8859-\* or ISO 2022-\*) and Unicode. For example, Shift-JIS encoding consists from JISX 0201 Roman (Japanese version of ISO 646), not ASCII, which encodes yen currency mark at 0x5c where backslash is encoded in ASCII.

Then which should your converter convert 0x5c in Shift-JIS into in Unicode, u+005c (backslash) or u+00a5 (yen currency mark)? You may say yen currency mark is the right solution. However, backslash (and then yen mark) is widely used for escape character. For example, 'new line' is expressed as 'backslash - n' in C string literal and Japanese people use 'yen currency mark - n'. You may say that program sources must written in ASCII and the wrong point is that you tried to convert program source. However, there are many source codes and so on written in Shift-JIS encoding.

Now Windows comes to support Unicode and the font at u+005c for Japanese version of Windows is yen currency mark. As you know, backslash (yen currency mark in Japan) is vitally important for Windows, because it is used to separate directory names. Fortunately, EUC-JP, which is widely used for UNIX in Japan, includes ASCII, not Japanese version of ISO 646. So this is not problem because it is clear 0x5c is backslash.

Thus all local codesets should not use character sets incompatible to ASCII, such as ISO 646-\*.


AFII contribution about WAVE DASH
---------------------------------

http://std.dkuug.dk/jtc1/sc2/wg2/docs/n2166.doc

::

  ISO/IEC JTC/1 SC/2 WG/2 N2166
  2000-01-04

**ISO/IEC JTC/1 SC/2 WG/2**

**Universal Multiple-Octet Coded Character Set (UCS)**

**Secretariat: ANSI**


:Title:
    U-301C  WAVE DASH

:Doc. Type:
    National body contribution
 
:Source:
	Japan -tks 

:Project:
	UCS

:Status:
	For review at WG2 meeting at Beijing or later

:Date:
	2000-01-04

:Distribution:
	ISO/IEC JTC1 SC2 WG2 

:Reference:
	ISO/IEC JTC1 SC2 WG2 N2030  
	AFII contribution about WAVE DASH

The WG2 N2030 (by AFII and also it is UTC-1999-022) is discussing about the shape and mapping issue of the U-301C.   It is read as:

1. Mapping issue:  U-301C should be mapped to X214 1(or 1-33) of JIS X 0208.

2. Glyph shape issue:  U-301C should have Unicode Ver. 3.0 shape which is almost like reversed tilde (at middle of character cell while tilde is top position of the cell).

3. Mapping to U-FF5E FULLWIDTH TILDE is (by any reason) mistake, even though some of implementation is doing such mapping.

The N2030 also describes that the purpose of U-301C is for compatibility purpose with the X-2141 (1-33 WABE DASH) of JIS X 0208.  And also describes that there are some of implementation that already map the U-301C to U+FF5E FULLWIDTH TILDE.

As an ownership country of JIS X 0208, Japan has strong comments as:

1. The U+301C should be mapped to X-2141 (1-33).   JIS version of the ISO/IEC 10646-1 (JIS X 0221:1995) is recommending this mapping in Japanese unique attachment.

2. The JIS X 0208 X-2141 (1-33) should not be mapped to U+FF5E FULLWIDTH TILDE.  The attachment of the JIS X 0221 clearly describes that the U-FF5E should be mapped to the 2-23 of JIS X 0212 when the ISO/IEC 646-IRV and JIS X 0212 (and JIS X 0208) are used simultaneously and double coding is prohibited. (Note that JIS X 0212 has TILDE at 2-21 as well as ISO/IEC 646-IRV at 7E)

3. Also, the new JIS (JIS X 0213:2000) does have “tilde” at code position of 1-2-18, therefore, it should be also mapped to TILDE (U-007E) or the FULLWIDTH TILDE(U-FF5E).

4. As a conclusion, Japan do not think the U-301C is a kind of TILDE by any reason, and thus, support the N2030 position on the mapping issue.

5. On the other hand, about the glyph shape of the U-301C, Japan does not support the recommended shape as same as the Unicode, Version 3.0 Draft as the N2030 says.  Japan, ideally, likes to see the shape like described in the N1796 (which is similar to tilde).

   a. JIS X 208 (X 2141 or 1-33) does have it’s shape like tilde (reversed from U-301C and the same as recommended in N1796).

   b. Japan thinks the tilde like or reversed are just a glyph variance of the same character (WAVE DASH) and either shape will do the job, but tilde like shape does have consistency with the printed JIS X 0208.

6. As a conclusion, Japan supports the mapping of U-301C described in the N2030, and recommending to change the glyph shape of the U-301C reversed (unlike N2030 recommended as Unicode V.3 daft  but want to see like N1796).

Japan hopes that this problem will be resolved in the Beijing WG2 meeting and eliminate the U-301C mapping to any of the TILDE family.
