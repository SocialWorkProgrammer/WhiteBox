package com.ssafy.whitebox.auth.dto;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class LoginRequest {

    private String user_email;
    private String user_password;

}