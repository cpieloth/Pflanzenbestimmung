<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <link rel="stylesheet" type="text/css" href="tree.css"/>
    <body>
      <xsl:for-each select="baeume/baum">
      <div>
        <xsl:value-of select="bezeichnung"/>
        <br/>
        <xsl:value-of select="gruppe"/>
      </div>
       </xsl:for-each>
    </body>
  </html> 
</xsl:template>

</xsl:stylesheet>
