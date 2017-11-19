Imports System.IO
Module Parrando
    'Simple and complex coin flips to move up and down stairs.
    'The paradox states that even though BOTH strategies lose
    'switching between them randomly guarantees that you will win.
    'in this case it is going up and down a series of 1001 stairs,
    '-500 through 0 through 500
    'if you try either strategy alone you will lose. together
    'you win. weird? Check it out:

    Dim randy As New System.Random
    Dim stair As Integer

    Sub Main()
        Dim game As Integer
        Dim counter As Integer = 0
        stair = 0

        Do
            game = randy.Next(1, 100)
            counter += 1
            If game <= 50 Then
                If counter Mod 1000 = 0 Then
                    Console.Out.WriteLine("called Simple at counter:" + counter.ToString + " and stair =" + stair.ToString + " ")
                End If
                Simple()
            Else
                If counter Mod 1000 = 0 Then
                    Console.Out.WriteLine("called Complex at counter:" + counter.ToString + " and stair =" + stair.ToString + " ")
                End If
                Complex()
            End If
        Loop While (stair < 500 And stair > -500)

        If stair >= 500 Then
            Console.Out.WriteLine("Winner")
        ElseIf stair <= -500 Then
            Console.Out.WriteLine("loser")
        Else
            Console.Out.WriteLine("error")
        End If

        Console.ReadKey()

    End Sub
    Sub Complex()
        ' This has a choice between flipping two coins.
        ' The "good" coin lands heads 74.5% of the time
        ' The "bad" coin lands heads only 9.5% of the time.
        ' per the paradox, you choose to flip the bad coin
        ' if the stair you are on is divisible by three.
        ' and roll the good coin, otherwise.
        Dim r As Integer
        If stair Mod 3 = 0 Then
            r = randy.Next(1, 1000)
            If r <= 95 Then
                stair += 1
            Else
                stair -= 1
            End If
        Else
            r = randy.Next(1, 1000)
            If r <= 745 Then
                stair += 1
            Else
                stair -= 1
            End If
        End If
    End Sub
    Sub Simple()
        ' you only flip one coin here, with a 49.5% chance to land heads
        ' and go up a stair, and 50.5% chance to land tails
        ' and go down a stair.
        Dim r As Integer
        r = randy.Next(1, 1000)
        If r <= 495 Then
            stair += 1
        Else
            stair -= 1
        End If
    End Sub
End Module

