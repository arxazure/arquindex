<?php
    // Criando nossas variáveis para guardar as informações do formulário
      $nome=$_POST['nome'];
    $email=$_POST['email'];
    $telefone=$_POST['telefone'];
    $deficiencia=$_POST['deficiencia'];
    $genero=$_POST['genero'];
    $pronomes=$_POST['pronomes'];
    $linkedin=$_POST['linkedin'];
    $tags=$_POST['tags'];
    $curriculo=$_POST['curriculo'];
    $consentimento=$_POST['consentimento'];
    $mensagem= 'Currículo Cadastrado Se Jogav<br><br>';
    $mensagem.='<b>Nome: </b>'.$nome.'<br>';
    $mensagem.='<b>E-Mail:</b> '.$email.'<br>';
    $mensagem.='<b>Telefone:</b> '.$telefone.'<br>';
    $mensagem.='<b>Deficiencia:</b> '.$deficiencia.'<br>';
    $mensagem.='<b>Genero:</b> '.$genero.'<br>';
    $mensagem.='<b>Pronomes:</b><br> '.$pronomes;
    $mensagem.='<b>Linkedin:</b><br> '.$linkedin;
    $mensagem.='<b>Tags:</b><br> '.$tags;
    $mensagem.='<b>Currículo:</b><br> '.$curriculo;
    $mensagem.='<b>Consentimento:</b><br> '.$consentimento;
    // abaixo as requisições do arquivo phpmailer
    require("phpmailer/src/PHPMailer.php");
    require("phpmailer/src/SMTP.php");
    require ("phpmailer/src/Exception.php");

    // chamando a função do phpmailer

$mail = new PHPMailer\PHPMailer\PHPMailer();
    $mail->isSMTP(); // Não modifique
    $mail->Host       = 'mail.arquindex.com.br';  // SEU HOST (HOSPEDAGEM)
    $mail->SMTPAuth   = true;                        // Manter em true
    $mail->Username   = 'marina.lopes@arquindex.com.br';   //SEU USUÁRIO DE EMAIL
    $mail->Password   = 'Marigabi123!';                   //SUA SENHA DO EMAIL SMTP password
    $mail->SMTPSecure = 'ssl';    //TLS OU SSL-VERIFICAR COM A HOSPEDAGEM
    $mail->Port       = 465;     //TCP PORT, VERIFICAR COM A HOSPEDAGEM
    $mail->CharSet = 'UTF-8';    //DEFINE O CHARSET UTILIZADO
    
    //Recipients
    $mail->setFrom('marina.lopes@arquindex.com.br', 'Site');  //DEVE SER O MESMO EMAIL DO USERNAME
    $mail->addAddress('arquindex@gmail.com');     // QUAL EMAIL RECEBERÁ A MENSAGEM!
    // $mail->addAddress('ellen@example.com');    // VOCÊ pode incluir quantos receptores quiser
    $mail->addReplyTo($email, $nome);  //AQUI SERA O EMAIL PARA O QUAL SERA RESPONDIDO                  
    // $mail->addCC('cc@example.com'); //ADICIONANDO CC
    // $mail->addBCC('bcc@example.com'); //ADICIONANDO BCC

    // Attachments
    // $mail->addAttachment('/var/tmp/file.tar.gz');         // Add attachments
    // $mail->addAttachment('/tmp/image.jpg', 'new.jpg');    // Optional name

    // Content
    $mail->isHTML(true);                                  // Set email format to HTML
    $mail->Subject = 'Cadastro Currículo Se Joga'; //ASSUNTO
    $mail->Body    = $mensagem;  //CORPO DA MENSAGEM
    $mail->AltBody = $mensagem;  //CORPO DA MENSAGEM EM FORMA ALT

    // $mail->send();
    if(!$mail->Send()) {
        echo "<script>alert('Erro ao enviar o E-Mail');window.location.assign('index.php');</script>";
     }else{
        echo "<script>alert('E-Mail enviado com sucesso!');window.location.assign('index.php');</script>";
     }
     die
?>