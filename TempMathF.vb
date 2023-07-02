Imports Microsoft.VisualBasic.Devices

Public Class Form1
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        TextBox1.Text = "90.0"
        TextBox2.Text = "60"
        REM Form1.Text = "Temperature Math"

    End Sub

    Private Sub TextBox1_TextChanged(sender As Object, e As EventArgs) Handles TextBox1.TextChanged
        Compute()
    End Sub

    Private Sub TextBox2_TextChanged(sender As Object, e As EventArgs) Handles TextBox2.TextChanged
        Compute()
    End Sub

    Private Sub Compute()
        Dim T As Double
        Dim RH As Double
        Dim Dewpoint As Double
        Dim HeatIndex As Double
        Dim WindChill As Double
        Dim WindSpeed As Double = 40.0
        Double.TryParse(TextBox1.Text, T)
        Double.TryParse(TextBox2.Text, RH)

        Dewpoint = T - ((9 / 25) * (100 - RH))
        HeatIndex = -42.379 + (2.04901523 * T) + (10.14333127 * RH) - (0.22475541 * T * RH) - (0.00683783 * T * T) - (0.05481717 * RH * RH) + (0.00122874 * T * T * RH) + (0.00085282 * T * RH * RH) - (0.00000199 * T * T * RH * RH)
        WindChill = 35.74 + (0.6215 * T) - (35.75 + (WindSpeed ^ 0.16)) + (0.4275 * T * (WindSpeed ^ 0.16))
        Dewpoint = Math.Round(Dewpoint, 2)
        HeatIndex = Math.Round(HeatIndex, 2)
        WindChill = Math.Round(WindChill, 0)
        Label3.Text = String.Format("{0}°F", Dewpoint)

        If T < 50.0 Then
            Label7.Text = String.Format("{0}°F", WindChill)
            Label8.Text = "Wind Chill at 40MPH"
            Label4.Text = ""
            Label6.Text = ""
        Else
            Label4.Text = String.Format("{0}°F", HeatIndex)
            Label6.Text = "Heat Index Approximate"
            Label7.Text = ""
            Label8.Text = ""

        End If
        If T > 118 Or HeatIndex > 118 Then
            Label4.ForeColor = Color.Red
            Label6.ForeColor = Color.Red
        Else
            Label4.ForeColor = Color.Black
            Label6.ForeColor = Color.Black
        End If

    End Sub


End Class
