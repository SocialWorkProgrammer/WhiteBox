package com.ssafy.whitebox.user.entity;

import com.ssafy.whitebox.user.dto.UserParam;
import com.ssafy.whitebox.user.util.UserType;
import jakarta.persistence.*;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Accessors(fluent = true)
@Entity
@NoArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_index")
    private Long userIndex;

    @Column(name = "user_nickname")
    private String userNickname;

    @Column(name="user_password", nullable = false)
    private String userPassword;

    @Column(name = "user_email", nullable = false)
    private String userEmail;

    // Enum 타입을 문자열로 저장할 것이다.
    @Enumerated(EnumType.STRING)
    @Column(name = "user_type" , nullable = false)
    private UserType userType;


    public User(String userNickname, String userPassword, String userEmail, UserType userType) {
        this(null, userNickname, userPassword, userEmail, userType);
    }

    public User(Long userIndex, String userNickname, String userPassword, String userEmail, UserType userType) {
        this.userIndex = userIndex;
        this.userNickname = userNickname;
        this.userPassword = userPassword;
        this.userEmail = userEmail;
        this.userType = userType;
    }

    public void changeType(UserType newType){
        this.userType = newType;
    }

    public Long getUserIndex() {
        return userIndex;
    }

    public String getUserNickname() {
        return userNickname;
    }

    public String getUserPassword() {
        return userPassword;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public UserType getUserType() {
        return userType;
    }
}
