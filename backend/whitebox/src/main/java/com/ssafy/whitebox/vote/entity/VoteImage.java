package com.ssafy.whitebox.vote.entity;

import com.ssafy.whitebox.user.entity.User;
import jakarta.persistence.*;
import lombok.*;
import com.ssafy.whitebox.ai.entity.AIResult;
import com.ssafy.whitebox.vote.entity.Vote;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "VOTE_IMAGE")
public class VoteImage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long imageId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "vote_id")
    private Vote vote;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_index")
    private User user;

    private String voImageUrl;
    private LocalDateTime voImageCreatedAt;
}
